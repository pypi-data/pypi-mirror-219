
import abc
from typing import Any
from pyttee.core import run_template 


class Builder:
    """
        Base interface of builder class  
    """

    @staticmethod
    def run_template(template, printer): 
        return run_template(template, printer)

    @abc.abstractmethod
    def printer(self, string) -> None:
        """
            Method that called in compilation time
            to store the compilator output
        """
        pass

    @abc.abstractmethod
    def __call__(self) -> Any:
        """
            The call of the builder class must return
            the result of the template processing
            of the current builder
        """
        pass


class TemplateNullBuilder(Builder):
    """
        Template builder that do compilation and returns
        nothing on __call__ This template builder made
        mainly for debug popouses
    """
    def __init__(self):
        pass

    def printer(self, string):
        pass

    def __call__(self, template):
        self.run_template(template, self.printer)
        return


class TemplateStrBuilder(Builder):
    """
        Template builder that compiles template and
        returns compilation result as string of html
    """

    def __init__(self):
        self.result = ""

    def printer(self, string):
        self.result += string

    def __call__(self, template):
        self.result = ""
        self.run_template(template, self.printer)
        return self.result

