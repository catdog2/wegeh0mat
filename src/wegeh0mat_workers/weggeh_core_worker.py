import worker
import logging
import util
import sqlite3
import datetime
from datetime import date

class WeggehWorker(worker.Worker):
    def __init__(self, config):
        super(WeggehWorker, self).__init__(config)
        
        self._db_connection = sqlite3.connect(self._config['sqlite'], 
                                              check_same_thread = False,
                                              detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        #now = datetime.datetime.now()
        #c = self._db_connection.cursor()
        #c.execute("insert into event values(2, 'moo', ?, ?, 'bar', null, 'cip', ?)", (now,now,now))
        #self._db_connection.commit()
        #c.close()
        
    def handle_command(self, origin, msg : dict, command : str, sendername : str, senderjid: str):
        if(util.starts_with_one_of(command.lower(), 'hilfe')):
            origin.handle_reply(msg, "%s: Dir ist nicht zu helfen!" % sendername)
        elif(util.starts_with_one_of(command.lower(), 'zeige alle verabredungen im detail')):
            origin.handle_reply(msg, self._get_event_list_str(all=True, details=True))
        elif(util.starts_with_one_of(command.lower(), 'zeige alle verabredungen')):
            origin.handle_reply(msg, self._get_event_list_str(all=True, details=False))
        elif(util.starts_with_one_of(command.lower(), 'zeige verabredungen im detail')):
            origin.handle_reply(msg, self._get_event_list_str(all=False, details=True))
        elif(util.starts_with_one_of(command.lower(), 'zeige verabredungen')):
            origin.handle_reply(msg, self._get_event_list_str(all=False, details=False))
        #elif()
            
    def _get_event_list_str(self, all : bool, details: bool):
        c = self._db_connection.cursor()
        
        now = datetime.datetime.now()
        q = 'select e.*, p.nickname, p.jid from event as e left outer join people as p '
        q += 'on e.id = p.id '
        if(all):
            c.execute(q)
        else:
            c.execute(q + "where e.end_date >= ? " + 
                      " or e.begin_date >= ?" , (now,now))
        
        
        rs = 'vorhandene Verabredungen:\n'
        result = c.fetchall()
        description = c.description
        c.close()
        
        for row in result:        
            rowdict = dict(zip([i[0] for i in description], row))
            begin_str =  rowdict['begin_date'].strftime("%a, %d.%m.%Y %H:%M Uhr") \
                if rowdict['begin_date'] != None else 'Unbekannt'
            end_str =  rowdict['end_date'].strftime("%a, %d.%m.%Y %H:%M Uhr") \
                if rowdict['begin_date'] != None else 'offen'
            
            if(details):
                rs += "#" + str(rowdict['id']) + ' ' + rowdict['name'] + ':\n'
                rs += "\tErsteller: " + str(rowdict['nickname']) + "\n"
                rs += "\tAnfang: " + begin_str + "\n"
                rs += "\tEnde: " + end_str + "\n"
                rs += "\tTreffpunkt: " + rowdict['meeting_point'] + "\n"
                rs += "\tKommentar: " + rowdict['comment'] + "\n"
            else:
                rs += '#' + str(rowdict['id']) + ' ' + rowdict['name'] + ' von ' + str(rowdict['creator'])
                rs += ' beginnt ' + begin_str + '\n' 
             
            

        return rs.rstrip("\n")
                