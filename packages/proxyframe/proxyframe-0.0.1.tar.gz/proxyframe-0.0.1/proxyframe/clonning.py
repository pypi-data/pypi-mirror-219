import attr
import logging

@attr.s
class CloneMaker:
    
    # inputs
    
    # inputs with defaults
    mess = attr.ib(default="CLONNING", type=str)
    shout_type = attr.ib(default="HEAD2", type=str)
    logger = attr.ib(default=logging)
    loggerLvl = attr.ib(default=logging.DEBUG)
    dotline_length = attr.ib(default=50, type=int)
  	
    def __attrs_post_init__(self):
        self.initialize_logger()
    
    def initialize_logger(self):
        
        logging.basicConfig(level=self.loggerLvl)
        logger = logging.getLogger('TnS')
        logger.setLevel(self.loggerLvl)
        
        self.logger = logger
        
   
    def shout(self):
        shoutOUT(type=self.shout_type, 
                 mess=self.mess, 
                 dotline_length=self.dotline_length,
                 logger=self.logger)


def shoutOUT(type="dline", 
             mess=None, 
             dotline_length=50,
             logger = logging):
    """
    Print a line of text with a specified length and format.

    Args:
        type (str): The type of line to print. Valid values are "dline" (default), "line", "pline", "HEAD1",
                    "title", "subtitle", "subtitle2", "subtitle3", and "warning".
        mess (str): The text to print out.
        dotline_length (int): The length of the line to print.

    Returns:
        None

    Examples:
        shoutOUT("HEAD1", mess="Header", dotline_length=50)
        shoutOUT(type="dline", dotline_length=50)
    """

    switch = {
        "dline": lambda: logger.info("=" * dotline_length),
        "line": lambda: logger.debug("-" * dotline_length),
        "pline": lambda: logger.debug("." * dotline_length),
        "HEAD1": lambda: logger.info("".join(["\n",
                                              "=" * dotline_length,
                                              "\n",
                                              "-" * ((dotline_length - len(mess)) // 2 - 1),
                                              mess,
                                              "-" * ((dotline_length - len(mess)) // 2 - 1),
                                              " \n",
                                              "=" * dotline_length])),
        "HEAD2": lambda: logger.info("".join(["\n",
                                              "*" * ((dotline_length - len(mess)) // 2 - 1),
                                              mess,
                                              "*" * ((dotline_length - len(mess)) // 2 - 1)])),
        "HEAD3": lambda: logger.info("".join(["\n",
                                              "/" * ((dotline_length - 10 - len(mess)) // 2 - 1),
                                              mess,
                                              "\\" * ((dotline_length - 10 - len(mess)) // 2 - 1)])),
        "title": lambda: logger.info(f"** {mess}"),
        "subtitle": lambda: logger.info(f"*** {mess}"),
        "subtitle2": lambda: logger.debug(f"+++ {mess}"),
        "subtitle3": lambda: logger.debug(f"++++ {mess}"),
        "warning": lambda: logger.warning(f"!!! {mess} !!!"),
    }

    switch[type]()  
