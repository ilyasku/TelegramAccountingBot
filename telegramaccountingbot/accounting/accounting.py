

class Bookkeeper:

    def __init__(self):
        self.persistence = None
        self.dict_id_to_name = None

    def set_persistence(self, persistence):
        self.persistence = persistence
        self.dict_id_to_name = persistence.get_dict_id_to_name()

    def add_transaction(self, _id, value, date, location):
        self.persistence.add_transaction(_id, value, date, location)

    def has_id(self, _id):
        for ID in self.dict_id_to_name.keys():
            if ID == _id:
                return True
        return False
        
    def get_balance(self):
        balance_dict = {}
        count = 0
        average = 0
        for _id in self.dict_id_to_name.keys():
            list_of_transactions = self.persistence.get_transactions(_id)
            _sum = self._sum_transactions(list_of_transactions)
            balance_dict[_id] = _sum
            average += _sum
            count += 1
        balance_dict["average"] = average / count
        return balance_dict

    def _sum_transactions(self, list_of_transactions):
        _sum = 0.0
        for t in list_of_transactions:
            _sum += t["value"]
        return _sum
