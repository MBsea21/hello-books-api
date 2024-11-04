class Point: 
    @classmethod 
    def create_instance_using_cls(cls):
        return cls()
    def create_instance_using_class_name(cls):
        return Point()

    