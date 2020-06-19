


class RowSetInfo:

    def __init__(self):
        self.restDataCollection = {}
        self.restDataColumnName = []

    def addRestData(self, columnName, restDataList):
        self.restDataColumnName.append(columnName)
        self.restDataCollection[columnName] = restDataList

    def popWritableData(self):
        writeableBuffer = {}
        for name in self.restDataColumnName:
            try:
                writeableBuffer[name] = self.restDataCollection[name].pop(0)
            except Exception as ex:
                print(ex)
                print("error col: ", name)

        for name in self.restDataColumnName.copy():
            if len(self.restDataCollection[name]) == 0:
                self.restDataColumnName.remove(name)

        if len(writeableBuffer) > 0:
            return writeableBuffer
        else:
            return None




