import worker
import logging
import util
import sqlite3
import datetime
import re
from datetime import date

participant_status_to_text = {"yes" : "Ja", "maybe" : "Vieleicht", "no" : "Nein", "invited" : "Eingeladen"}

class WeggehWorker(worker.Worker):
    def __init__(self, config):
        super(WeggehWorker, self).__init__(config)
        
        self._db_connection = sqlite3.connect(self._config['sqlite'],
                                              check_same_thread=False,
                                              detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        # now = datetime.datetime.now()
        # c = self._db_connection.cursor()
        # c.execute("insert into event values(2, 'moo', ?, ?, 'bar', null, 'cip', ?)", (now,now,now))
        # self._db_connection.commit()
        # c.close()
        
    def handle_command(self, origin, msg : dict, command : str, sendername : str, senderjid: str):
        if util.starts_with_one_of(command.lower(), 'hilfe'):
            origin.handle_reply(msg, "%s: Dir ist nicht zu helfen!" % sendername)
        elif util.starts_with_one_of(command.lower(), 'zeige alle vorschläge im detail'):
            origin.handle_reply(msg, self._get_event_list_str(all=True, details=True))
        elif util.starts_with_one_of(command.lower(), 'zeige alle vorschläge'):
            origin.handle_reply(msg, self._get_event_list_str(all=True, details=False))
        elif util.starts_with_one_of(command.lower(), 'zeige vorschläge im detail'):
            origin.handle_reply(msg, self._get_event_list_str(all=False, details=True))
        elif util.starts_with_one_of(command.lower(), 'zeige vorschläge'):
            origin.handle_reply(msg, self._get_event_list_str(all=False, details=False))
        elif util.starts_with_one_of(command.lower(), 'setze status in vorschlag'):
            id = None
            status = None
            try:
                p = re.compile('.*setze\s+status\s+in\s+vorschlag\s+([0-9]+)\s+auf\s+(.+)')
                match = p.match(command.lower())
                id = int(match.groups()[0])
                psttreversed = dict([(participant_status_to_text[k].lower(), k) for k in participant_status_to_text])
                if status not in psttreversed:
                    origin.handle_reply(msg, "Ungültiger status!")
                    return
                status = psttreversed[match.groups()[1]]
            except Exception as e:
                logging.getLogger().debug("unable to parse setze status: %s" % str(e))
                return            
            origin.handle_reply(msg, self.__handle_status_change(self, id, status, sendername, senderjid))
        elif util.starts_with_one_of(command.lower(), 'neuer vorschlag'):
            
            date = None
            name = None
            
            try:
                p = re.compile('.*neuer\s+vorschlag,?\s+(.+)\s+am\s+(.+)')
                match = p.match(command)
                name = match.groups()[0]
                
                date = datetime.datetime.strptime(match.groups()[1], "%d.%m.%Y um %H:%M")
            except Exception as e:
                logging.getLogger().debug("unable to parse vorschlag: %s" % str(e))
                return    
            
            origin.handle_reply(msg, self._handle_vorschlag(name, date, sendername, senderjid))


    def _handle_status_change(self, eventid, status, sendername, senderjid):
        c = self._db_connection.cursor()
        c.execute("select id from people where nickname = ? or jid = ?", (sendername, senderjid))
        nameresult = c.fetchone()
        userid = -1
        
        if nameresult == None:
            
            c = self._db_connection.cursor()
            c.execute("select max(id) from people")
            userid = c.fetchone()
            creatorid = maxresult[0] + 1
            c.execute("insert  into people (id,nickname,jid) values(?,?,?)", (creatorid, sendername, senderjid))
            
        else:
            userid = nameresult[0]
            
        c.execute("insert into participants (event_id, people_id, status)" + 
                  "values(?,?,?)", (eventid , userid, status))        

        self._db_connection.commit()
        c.close() 

    def _handle_vorschlag(self, name: str, date: datetime.datetime, sendername, senderjid) -> str:
        c = self._db_connection.cursor()
        c.execute("select id from people where nickname = ? or jid = ?", (sendername, senderjid))
        nameresult = c.fetchone()
        creatorid = -1
        
        if nameresult == None:
            
            c = self._db_connection.cursor()
            c.execute("select max(id) from people")
            maxresult = c.fetchone()
            creatorid = maxresult[0] + 1
            c.execute("insert  into people (id,nickname,jid) values(?,?,?)", (creatorid, sendername, senderjid))
            
        else:
            creatorid = nameresult[0]
            
        now = datetime.datetime.now()
        c.execute("select max(id) + 1 from event")
        maxresult = c.fetchone()
        
        c.execute("insert into event (id, name, begin_date, create_date, creator) " + 
                      "values(?, ?,?,?,?)", (maxresult[0], name, date, now, creatorid))
        c.execute("insert into participants (event_id, people_id, status)" + 
                  "values(?,?,'yes')", (maxresult[0], creatorid))
        
        self._db_connection.commit()
        
        c.close() 
        
        return "Vorschlag #%d erstellt!" % maxresult[0]        
            
    def _get_event_list_str(self, all : bool, details: bool):
        c = self._db_connection.cursor()
        
        now = datetime.datetime.now()
        q = 'select e.*, p.nickname, p.jid from event as e left outer join people as p '
        q += 'on e.id = p.id '
        if(all):
            c.execute(q)
        else:
            c.execute(q + " where e.end_date >= ? " + 
                      " or e.begin_date >= ?" , (now, now))
        
        
        rs = 'vorhandene Vorschläge:\n'
        eventresult = c.fetchall()
        eventdescription = c.description
        
        
        for row in eventresult:   
            rowdict = dict(zip([i[0] for i in eventdescription], row))
            
            c.execute("select p.nickname, p.jid, par.status p from participants as par, people as p " + 
                      " where par.event_id = ? and par.people_id = p.id", (rowdict['id'],))
            partiresult = c.fetchall()
            

            begin_str = rowdict['begin_date'].strftime("%a, %d.%m.%Y %H:%M Uhr") \
                if rowdict['begin_date'] != None else 'Unbekannt'
            end_str = rowdict['end_date'].strftime("%a, %d.%m.%Y %H:%M Uhr") \
                if rowdict['end_date'] != None else 'offen'
            
            cntstr = lambda str: sum([1 for i in partiresult if i[2] == str])
            particountstr = "%d Ja, %d Nein, %d Vieleicht, %d Eingeladen" % \
                (cntstr("yes"), cntstr("no"), cntstr("maybe"), cntstr("invited"))
            
            if(details):
                rs += "#" + str(rowdict['id']) + ' ' + rowdict['name'] + ':\n'
                rs += "\tErsteller: " + str(rowdict['nickname']) + "\n"
                rs += "\tAnfang: " + begin_str + "\n"
                rs += "\tEnde: " + end_str + "\n"
                rs += "\tTreffpunkt: " + str(rowdict['meeting_point']) + "\n"
                rs += "\tKommentar: " + str(rowdict['comment']) + "\n"
                rs += "\tTeilnehmerzahl: " + particountstr + "\n"
                rs += "\tTeilnehmer: "
                for parti in partiresult:
                     rs += "%s (%s), " % (parti[0], participant_status_to_text[parti[2]])
                rs = rs[:-2] + "\n"
            else:
                rs += '#' + str(rowdict['id']) + ' ' + rowdict['name'] + ' von ' + str(rowdict['nickname'])
                rs += ' beginnt ' + begin_str + " (%s) \n" % particountstr
             
        c.close()     


        return rs.rstrip("\n")
                
