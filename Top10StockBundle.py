"""
This is a template algorithm on Quantopian for you to adapt and fill in.
"""
from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import AverageDollarVolume
from quantopian.pipeline.data import morningstar
from quantopian.pipeline.filters.morningstar import Q1500US
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pandas as pd
tickerCollection = []
dayCounter = 0

 
def preview(df):
    log.info(df.head())        
    return df
    

def initialize(context):
    
    context.stock_list = [sid(24)]
    context.min_stock = sid(24)
    
    
    """
    Called once at the start of the algorithm.
    """ 
    
    fetch_csv('https://www.dl.dropboxusercontent.com/s/jtxuk0152xp7m6o/NEWSCORES.csv?dl=0', date_column='Date', date_format='%m/%d/%y', pre_func=preview)
    
    context.stocks = symbols('AAPL', 'MSFT')    
    #print context.tradeable.size
    
    # Rebalance every day, 1 hour after market open.
    schedule_function(my_daily_trade, date_rules.every_day(), time_rules.market_open(hours=1))
     
    # Record tracking variables at the end of each day.
    schedule_function(my_record_vars, date_rules.every_day(), time_rules.market_close())
     
    today = get_datetime()   
    #one_year_ago = today - relativedelta(years=1)
    
    # Create our dynamic stock selector.
    pipe = attach_pipeline(make_pipeline(), 'pipe')

    ebitda = morningstar.income_statement.ebitda.latest
    long_term_debt = morningstar.balance_sheet.long_term_debt.latest
    #long_term_debty2 = morningstar.balance_sheet.long_term_debt.one_year_ago
    enterprise_value = morningstar.valuation.enterprise_value.latest
    market_cap = morningstar.valuation.market_cap.latest
                                 
    pipe.add(ebitda, 'ebitda')  
    pipe.add(long_term_debt, 'long_term_debt')
    pipe.add(enterprise_value, 'enterprise_value')
    pipe.add(market_cap, 'market_cap')

    nonzero = (ebitda != 0)
    ev_eb = enterprise_value/ebitda
    ev_eb_ratio = ev_eb.percentile_between(0,50)
    ltd_eb = long_term_debt/ebitda
    ltd_eb_ratio = ltd_eb.percentile_between(50,100)
    percentile = market_cap.percentile_between(25,75)
    
    pipe.set_screen(nonzero & ev_eb_ratio & ltd_eb_ratio & percentile, overwrite=True)
                                 
    
    
    
         
def make_pipeline():
    """
    A function to create our dynamic stock selector (pipeline). Documentation on
    pipeline can be found here: https://www.quantopian.com/help#pipeline-title
    """
    
    # Base universe set to the Q500US
    base_universe = Q1500US()

    # Factor of yesterday's close price.
    yesterday_close = USEquityPricing.close.latest
     
    pipe = Pipeline(
        screen = base_universe,
        columns = {
            'close': yesterday_close,
        }
    )
    return pipe
 
def before_trading_start(context, data):
    """
    Called every day before market open.
    """
    """
    context.output = pipeline_output('pipe')
  
    # These are the securities that we are interested in trading each day.
    context.security_list = context.output.index
    """
     
def my_assign_weights(context, data):
    """
    Assign weights to securities that we want to order.
    """
    pass
 
def my_daily_trade(context,data):
    """
    Execute orders according to our schedule_function() timing. 
    """
    context.output = pipeline_output('pipe')

    context.security_list = context.output.index
    """
    print("stock list: ")
    for stock in context.security_list:
        print(stock)
    """ 
    """
    last_date_str = data.current(sid(24), 'indicatorDate')
    last_date = datetime.strptime(last_date_str, "%m/%d/%y")
    today = str(get_datetime(None))
    today_date = datetime.strptime(today[0:10], "%Y-%m-%d")
    difference = (today_date - last_date).days
    print difference
    """
    
    global dayCounter
    
    print len(context.security_list)
    #buy top 10 stocks to start
    if dayCounter == 0 or len(context.stock_list) < 10:  
        minval = -1 
        for stock in context.security_list:
            if len(context.stock_list) < 10:
                context.stock_list.append(stock)
                if data.current(stock, 'indicator') >= minval:
                   context.min_stock = stock
                   minval = data.current(stock, 'indicator')
            else:
                   if data.current(stock, 'indicator') >= minval:
                       context.stock_list.append(stock)
                       context.stock_list.remove(context.min_stock)
                       context.min_stock = stock
                       minval = data.current(stock, 'indicator')
                   
        for stock in context.stock_list:
             order_target_percent(stock, 1.0/10)
                   
        
        
    else:
        today = str(get_datetime(None))
        today_date = datetime.strptime(today[0:10], "%Y-%m-%d")
        for stock in context.security_list:
            if data.can_trade(stock):
                last_date_str = str(data.current(stock, 'indicatordate'))
                if(last_date_str != 'nan'):
                    
                    last_date = datetime.strptime(last_date_str, "%m/%d/%y")
                    #check if new transcript came out today
                    if (today_date-last_date).days == 0:
                        new_score = data.current(stock, 'indicator')
                        if new_score < data.current(context.min_stock, 'indicator'):
                            order_target_percent(context.min_stock, 0)
                            context.stock_list.remove(context.min_stock)
                            order_target_percent(stock, 1.0/10)
                            context.stock_list.append(stock)
                            updateMin(context, data)
                        
    print len(context.stock_list)   
    dayCounter = dayCounter + 1                     
    pass
 
def updateMin(context, data):
    minval = -1
    for stock in context.stock_list:
        if data.current(stock, 'indicator') >= minval:
            context.min_stock = stock
            minval = data.current(stock, 'indicator')
        

        
    
    
def my_record_vars(context, data):
    """
    Plot variables at the end of each day.
    """
    pass
 
def handle_data(context,data):

    pass
