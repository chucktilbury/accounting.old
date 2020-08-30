import os
import time, locale

import sqlite3 as sql
import tkinter as tk
from tkinter import messagebox as mbox
from logger import *

@class_wrapper
class Database(object):
    '''
    The goal of this class is to move all SQL composition out of the program
    logic and place it here.
    '''

    __instance = None

    @staticmethod
    def get_instance():
        '''
        This static method is used to get the singleton object for this class.
        '''
        if Database.__instance == None:
            Database()
        return Database.__instance

    def __init__(self):

        # gate the access to __init__()
        if Database.__instance != None:
            raise Exception("Database class is a singleton. Use get_instance() instead.")
        else:
            Database.__instance = self

        # Continue with init exactly once.
        self.data_version = '1.0'
        self.database_name = 'sql/accounting.db'
        self.db_create_file = 'sql/database.sql'
        self.db_pop_file = 'sql/populate.sql'
        self.open()
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        self.logger.set_level(Logger.INFO)

    @func_wrapper
    def open(self):

        if not os.path.isfile(self.database_name):
            self.create_database()

        self.db = sql.connect(self.database_name)
        self.db.row_factory = sql.Row

    @func_wrapper
    def close(self):
        self.db.commit()
        self.db.close()

    @func_wrapper
    def read_statement(self, fh):
        '''
        Read a statement from the *.sql file and return it. This skips comments and concatinates lines
        until a ';' is read.

        A comment is text that starts with a '#' and continues to the end of the line.
        '''
        retv = ''
        for line in fh:
            # strip comments from the line
            idx = line.find('#')
            line = line[0:idx].strip()
            # If there is anything left, append it to the return value.
            if len(line) > 0:
                retv += " %s"%(line)
                if line[-1] == ';':
                    break

        return retv

    @func_wrapper
    def run_file(self, db, name):
        '''
        Execute all of the statements in a *.sql file.
        '''

        with open(name) as fh:
            while True:
                line = self.read_statement(fh)
                if len(line) > 0:
                    db.execute(line)
                else:
                    break

    @func_wrapper
    def create_database(self):
        '''
        Create the database if it does not exist already.
        '''
        # Load the DB creation file and create the database from that.

        c = sql.connect(self.database_name)
        db = c.cursor()
        self.run_file(db, self.db_create_file)
        self.run_file(db, self.db_pop_file)
        c.commit()
        c.close()

    @func_wrapper
    def get_columns(self, table):
        '''
        Return a dict where all column names are keys with blank data.
        '''
        # TODO: make the data the type of element that the column uses.
        retv = {}
        cols = self.execute('PRAGMA table_info(%s);' % (table))
        for item in cols:
            retv[item[1]] = ''
        return cols

    @func_wrapper
    def get_column_list(self, table):
        '''
        Return a list with all of the column names.
        '''
        retv = []
        cols = self.execute('PRAGMA table_info(%s);' % (table))
        for item in cols:
            retv.append(item[1])
        return retv

    @func_wrapper
    def execute(self, sql):
        '''
        Execute an arbitrary SQL statement.
        '''
        return self.db.execute(sql)

    @func_wrapper
    def commit(self):
        '''
        Commit the database to disk.
        '''
        self.db.commit()

    @func_wrapper
    def populate_list(self, table, column):
        '''
        Return a list with all of the items then the column of the table.
        '''
        curs = self.execute('select %s from %s;'%(column, table))
        retv = []
        for item in curs:
            retv.append(' '.join(item))
            #retv.append(item)
        return retv

    @func_wrapper
    def get_row_by_id(self, table, ID):
        '''
        Return a dict of all of the columns in the row that has the specified ID.
        '''
        curs = self.execute('select * from %s where ID = %d;'%(table, ID)).fetchall()
        try:
            retv = dict(curs[0])
            return retv
        except IndexError:
            return None

    @func_wrapper
    def get_id_by_row(self, table, col, val):
        '''
        Return a dictionary of the columns in the row where a data element matches the value given.
        '''
        if type(val) is str:
            sql = 'SELECT ID FROM %s WHERE %s = \"%s\";'%(table, col, val)
        else:
            sql = 'SELECT ID FROM %s WHERE %s = %s;'%(table, col, val)
        row = self.execute(sql).fetchall()

        if len(row) == 0:
            return None
        else:
            return dict(row[0])['ID']

    @func_wrapper
    def get_cursor(self):
        '''
        Return the current database cursor.
        '''
        return self.db.cursor()

    @func_wrapper
    def get_id_list(self, table, where=None):
        '''
        Get a list of all of the IDs in the table
        '''
        retv = []
        if where is None:
            sql = 'SELECT ID FROM %s;'%(table)
        else:
            sql = 'SELECT ID FROM %s WHERE %s;'%(table, where)
        cur = self.execute(sql)
        for item in cur:
            retv.append(item[0])

        return retv

    @func_wrapper
    def get_row_list(self, table, where):
        '''
        Get a generic list of rows based on more than one criteria
        '''
        retv = []
        sql = 'SELECT * FROM %s WHERE %s'%(table, where)
        cur = self.execute(sql)
        for item in cur:
            retv.append(dict(item))

        if len(retv) == 0:
            return None
        else:
            return retv

    @func_wrapper
    def get_row_list_by_col(self, table, col, val):
        '''
        Get the list of all rows where the column has a certain value
        '''
        retv = []
        if type(val) is str:
            sql = 'SELECT * FROM %s WHERE %s = \"%s\";'%(table, col, val)
        else:
            sql = 'SELECT * FROM %s WHERE %s = %s;'%(table, col, val)

        cur = self.execute(sql)
        for item in cur:
            retv.append(dict(item))

        if len(retv) == 0:
            return None
        else:
            return retv

    @func_wrapper
    def get_id_by_name(self, table, col, val):
        '''
        Return the ID where the data in the column matches the value. Only returns the
        first match.
        '''
        if type(val) is str:
            sql = 'select ID from %s where %s = \"%s\";'%(table, col, val)
        else:
            sql = 'select ID from %s where %s = %s;'%(table, col, str(val))

        curs = self.execute(sql)
        recs = curs.fetchall()

        retv = None
        for row in recs:
            retv =  row[0]
            break

        return retv

    @func_wrapper
    def get_single_value(self, table, col, row_id):
        '''
        Retrieve a single value where the table, column and row ID are known.
        '''
        sql = 'SELECT %s FROM %s WHERE ID=%d;'%(col, table, row_id)
        curs = self.execute(sql)
        recs = curs.fetchall()

        retv = None
        for row in recs:
            retv =  row[0]
            break

        return retv

    @func_wrapper
    def set_single_value(self, table, col, row_id, val):
        '''
        Retrieve a single value where the table, column and row ID are known.
        '''
        vals = tuple([val])
        sql = 'UPDATE %s SET %s=? WHERE ID=%d;'%(table, col, row_id)

        return self.db.execute(sql, vals)

    @func_wrapper
    def insert_row(self, table, rec):
        '''
        Insert a row from a dictionary. This expects a dictionary where the keys are the column names and
        the values are to be inserted in to the columns.
        '''
        keys = ','.join(rec.keys())
        qmks = ','.join(list('?'*len(rec)))
        vals = tuple(rec.values())

        sql = 'INSERT INTO %s (%s) VALUES (%s);'%(table, keys, qmks)
        return self.db.execute(sql, vals).lastrowid

    @func_wrapper
    def update_row(self, table, rec, where):
        '''
        Update a row from a dictionary. This expects a dictionary where the keys are the column names and
        the data is the value to place in those columns. A condition must be specified, such as ID=123.
        Otherwise the database will have incorrect data placed in it.
        '''
        keys = '=?,'.join(rec.keys())
        keys += '=?'
        vals = tuple(rec.values())

        sql = 'UPDATE %s SET %s WHERE %s;'%(table, keys, where)
        return self.db.execute(sql, vals)

    @func_wrapper
    def update_row_by_id(self, table, rec, id):
        '''
        Update a row using a dictionary and the id of the row. This expects a dictionary where the keys are
        the column names and the data is the value to be placed in the columns.
        '''
        keys = '=?,'.join(rec.keys())
        keys += '=?'
        vals = tuple(rec.values())

        sql = 'UPDATE %s SET %s WHERE ID = %d;'%(table, keys, id)
        return self.db.execute(sql, vals)

    @func_wrapper
    def delete_row(self, table, id):
        '''
        Delete the row given by the ID
        '''
        sql = 'DELETE FROM %s WHERE ID = %d;' % (table, id)
        return self.db.execute(sql)

    @func_wrapper
    def delete_where(self, table, where):
        '''
        Delete rows that conform to the "where" clause.
        '''
        sql = 'DELETE FROM %s WHERE %s;' % (table, where)
        return self.db.execute(sql)

    @func_wrapper
    def if_rec_exists(self, table, column, value):
        '''
        Return True if there is a row that has the column with the value
        '''
        if type(value) is int or type(value) is float:
            sql = 'SELECT %s FROM %s WHERE %s = %s;'%(column, table, column, str(value))
        else:
            sql = 'SELECT %s FROM %s WHERE %s = \"%s\";'%(column, table, column, value)
        cursor = self.db.execute(sql)
        if cursor.fetchone() is None:
            return False

        return True

    @func_wrapper
    def convert_value(self, val, value_type, abs_val=True):
        '''
        Convert the value to the specified type. The value_type is an actual python type name.
        '''
        retv = None
        #try:
        if type(val) is value_type:
            retv = val
        elif value_type is str:
            retv = str(val)
        else:
            if value_type is float:
                if type(val) is str:
                    if val == '':
                        retv = 0.0
                    else:
                        if abs_val:
                            retv = abs(locale.atof(val))
                        else:
                            retv = locale.atof(val)
                else:
                    if abs_val:
                        retv = abs(locale.atof(val))
                    else:
                        retv = locale.atof(val)

            elif value_type is int:
                if abs_val:
                    retv = int(abs(locale.atof(val)))
                else:
                    retv = int(locale.atof(val))
        # except:
        #     self.logger.error('Cannot convert value')
        #     exit(1)

        return retv
