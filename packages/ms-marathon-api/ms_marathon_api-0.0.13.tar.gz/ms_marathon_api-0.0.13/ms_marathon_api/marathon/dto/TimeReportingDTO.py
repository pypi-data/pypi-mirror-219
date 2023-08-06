class TimeReportingDTO:
    def __init__(
        self,
        company,
        employee,
        msemail,
        client,
        clientname,
        project,
        mscode,
        feecode,
        accountingdate,
        recorddate,
        minutes,
    ):
        self.company = company
        self.employee = employee
        self.msemail = msemail
        self.client = client
        self.clientname = clientname
        self.project = project
        self.mscode = mscode
        self.feecode = feecode
        self.accountingdate = accountingdate
        self.recorddate = recorddate
        self.minutes = minutes

    def _get_record_value(self, record, column_name):
        try:
            return record[column_name]
        except KeyError:
            return None

    @staticmethod
    def load_data(record):
        return TimeReportingDTO(
            company=record["company"],
            employee=record["employee"],
            msemail=record["msemail"],
            client=record["client"],
            clientname=record["clientname"],
            project=record["project"],
            mscode=record["mscode"],
            feecode=record["feecode"],
            accountingdate=record["accountingdate"],
            recorddate=record["recorddate"],
            minutes=record["minutes"],
        )

    def to_dict(self):
        return {
            "company": self.company,
            "employee": self.employee,
            "msemail": self.msemail,
            "client": self.client,
            "clientname": self.clientname,
            "project": self.project,
            "mscode": self.mscode,
            "feecode": self.feecode,
            "accountingdate": self.accountingdate,
            "recorddate": self.recorddate,
            "minutes": self.minutes,
        }
