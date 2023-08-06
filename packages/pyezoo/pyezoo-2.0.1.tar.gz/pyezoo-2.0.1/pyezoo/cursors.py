class Cursor:
    """
    This is the object used to interact with the database.

    Do not create an instance of a Cursor yourself. Call
    connections.Connection.cursor().

    These objects represent a database cursor, which is used to manage the context of a fetch operation. Cursors created
    from the same connection are not isolated, i.e., any changes done to the database by a cursor are immediately
    visible by the other cursors. Cursors created from different connections can or can not be isolated, depending on
    how the transaction support is implemented (see also the connection's .rollback() and .commit() methods).

    """

    def __init__(self, connection):
        self.connection = connection
        self.description = None
        self.rowcount = -1
        self.rownumber = 0
        self.arraysize = 1
        self._executed = None
        self._result = None
        self._rows = None

    def close(self):
        """
        Closing a cursor just exhausts all remaining data.
        """
        conn = self.connection
        if conn is None:
            return
        try:
            while self.nextset():
                pass
        finally:
            self.connection = None

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        del exc_info
        self.close()

    def callproc(self, procname, args=()):
        """
        This method is optional since not all databases provide stored procedures.
        """
        pass

    def execute(self, query, args=None):
        """Execute a query.

        :param query: Query to execute.
        :type query: str

        :param args: Parameters used with query. (optional)
        :type args: tuple, list or dict

        :return: Number of affected rows.
        :rtype: int

        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """
        while self.nextset():
            pass

        query = self.mogrify(query, args)

        result = self._query(query)
        self._executed = query
        return result

    def executemany(self, query, args):
        """Run several data against one query.

        :param query: Query to execute.
        :type query: str

        :param args: Sequence of sequences or mappings. It is used as parameter.
        :type args: tuple or list

        :return: Number of rows affected, if any.
        :rtype: int or None

        This method improves performance on multiple-row INSERT and
        REPLACE. Otherwise it is equivalent to looping over args with
        execute().
        """
        if not args:
            return

        m = RE_INSERT_VALUES.match(query)
        if m:
            q_prefix = m.group(1) % ()
            q_values = m.group(2).rstrip()
            q_postfix = m.group(3) or ""
            assert q_values[0] == "(" and q_values[-1] == ")"
            return self._do_execute_many(
                q_prefix,
                q_values,
                q_postfix,
                args,
                self.max_stmt_length,
                self._get_db().encoding,
            )

        self.rowcount = sum(self.execute(query, arg) for arg in args)
        return self.rowcount

    def fetchone(self):
        """Fetch next row."""
        self._check_executed()
        row = self.read_next()
        if row is None:
            return None
        self.rownumber += 1
        return row

    def fetchall(self):
        """
        Fetch all, as per MySQLdb. Pretty useless for large queries, as
        it is buffered. See fetchall_unbuffered(), if you want an unbuffered
        generator version of this method.
        """
        return list(self.fetchall_unbuffered())

    def nextset(self):
        """
        This method is optional since not all databases support multiple result sets.

        This method will make the cursor skip to the next available set, discarding any remaining rows from the current
        set.
        If there are no more sets, the method returns None. Otherwise, it returns a true value and subsequent calls to
        the .fetch*() methods will return rows from the next result set.
        """
        pass

    def setinputsizes(self, *args):
        """Does nothing, required by DB API."""
        pass

    def setoutputsizes(self, *args):
        """Does nothing, required by DB API."""
        pass
