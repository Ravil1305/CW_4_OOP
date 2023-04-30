class Vacancy:

    def __init__(self, title, salary, description, url):
        self.title = title
        self.salary = salary
        self.description = description
        self.url = url

    def __str__(self):
        return f"{self.title} \n{self.salary} \n{self.description} \nURL: {self.url}"
