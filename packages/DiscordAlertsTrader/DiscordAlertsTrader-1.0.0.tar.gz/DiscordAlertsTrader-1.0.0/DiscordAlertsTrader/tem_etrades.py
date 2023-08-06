import pandas as pd

import webbrowser
import json
from rauth import OAuth1Service


from DiscordAlertsTrader.configurator import cfg
from DiscordAlertsTrader.brokerages import BaseBroker

import pyetrade
oauth = pyetrade.ETradeOAuth(cfg["etrade"]["CONSUMER_KEY"],cfg["etrade"]["CONSUMER_SECRET"])

print(oauth.get_request_token())  # Use the printed URL

verifier_code = input("Enter verification code: ")
tokens = oauth.get_access_token(verifier_code)
print(tokens)

accounts = pyetrade.ETradeAccounts(
    cfg["etrade"]["CONSUMER_KEY"],
    cfg["etrade"]["CONSUMER_SECRET"],
    tokens['oauth_token'],
    tokens['oauth_token_secret']
)


# lists all the accounts for
accounts_resp = accounts.list_accounts(resp_format='json')

accountIDKey = '<Key for the chosen account from list_accounts>'


account_choices = (
            accounts_resp.get("AccountListResponse", {})
            .get("Accounts", {})
            .get("Account", [])
        )
accounts_kv = {account["accountId"]: account["accountIdKey"] for account in account_choices}
        
# Prints account balance
for k,v in accounts_kv.items():
    print(accounts.get_account_balance(v, resp_format='json'))
print(accounts.get_account_balance('dBZOKt9xDrtRSAOl4MSiiA', resp_format='json'))


class TDA(BaseBroker):
    def __init__(self):
        pass

    def get_session(self, account_n=0, accountId=None):
        """Provide either:
            - account_n: indicating the orinal position from the accounts list
            (if only one account, it will be 0)
            - accountId: Number of the account

        auth is a dict with login info created with setup.py
        """
        if len(cfg['TDA']['client_id']) < 10:
            raise ValueError( "No TDA authentication file found, get credentials (in setup.py) to continue")
        # Create a new session, credentials path is required.
        self.session = TDClient(
            client_id=cfg['TDA']['client_id'],
            redirect_uri=cfg['TDA']['redirect_url'],
            credentials_path=cfg['TDA']['credentials_path']
        )

    def oauth():
        """Allows user authorization for the sample application with OAuth 1"""
        etrade = OAuth1Service(
            name="etrade",
            consumer_key=cfg["etrade"]["CONSUMER_KEY"],
            consumer_secret=cfg["etrade"]["CONSUMER_SECRET"],
            request_token_url="https://api.etrade.com/oauth/request_token",
            access_token_url="https://api.etrade.com/oauth/access_token",
            authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
            base_url="https://api.etrade.com")
        
        base_url = cfg["etrade"]["SANDBOX_BASE_URL"]

        request_token, request_token_secret = etrade.get_request_token(
            params={"oauth_callback": "oob", "format": "json"})

        # Go through the authentication flow. Login to E*TRADE.
        # After you login, the page will provide a verification code to enter.
        authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
        webbrowser.open(authorize_url)
        text_code = input("Please accept agreement and enter verification code from browser: ")

        session = etrade.get_auth_session(request_token,
                                    request_token_secret,
                                    params={"oauth_verifier": text_code})

        url = base_url + "/v1/accounts/list.json"
        
        # Make API call for GET request
        response = session.get(url, header_auth=True)

        
        processed = json.loads(response.content)
        
        
        account_choices = (
            processed.get("AccountListResponse", {})
            .get("Accounts", {})
            .get("Account", [])
        )
        accounts = {account["accountId"]: account["accountIdKey"] for account in account_choices}
        # Login to the session
        success = self.session.login()

        if accountId is not None:
            self.session.accountId = accountId
        else:
            account_n = 0
            accounts_info = self.session.get_accounts(account="all")[account_n]
            self.session.accountId = accounts_info['securitiesAccount']['accountId']
        return success
    def choose_account(self, account_id):
        url = f"{_BASE_URL}/v1/accounts/list.json"
        response = self.session.get(url)

        if response.status_code != 200:
            return False

        processed = json.loads(response.content)
        account_choices = (
            processed.get("AccountListResponse", {})
            .get("Accounts", {})
            .get("Account", [])
        )

        # discard dashes in account_id
        account_id = account_id.replace("-", "")

        # account_id -> account_id_key
        accounts = {account["accountId"]: account["accountIdKey"] for account in account_choices}
        if account_id not in accounts:
            return False

        # selected account := account_id_key
        self.selected_account = accounts[account_id]
        return True

    def cash_available(self):
        params = {"instType": "BROKERAGE", "realTimeNAV": "true"}
        headers = {"consumerkey": self.key}

        url = f"{_BASE_URL}/v1/accounts/{self.selected_account}/balance.json"

        response = self.session.get(
            url, header_auth=True, params=params, headers=headers
        )

        if response.status_code != 200:
            return False

        resp = json.loads(response.content)

        return resp["BalanceResponse"]["Computed"]["cashAvailableForInvestment"]

    def positions(self) -> json:
        url = f"{_BASE_URL}/v1/accounts/{self.selected_account}/portfolio.json"
        response = self.session.get(url, header_auth=True)

        if response.status_code != 200:
            return None

        content = json.loads(response.content)

        print(content)

        return response.content

    def quote(self, symbol: str, detail: QuoteDetail = None) -> json:
        if detail is None:
            url = f"{_BASE_URL}/v1/market/quote/{symbol}"
        else:
            url = f"{_BASE_URL}/v1/market/quote/{symbol}?detailFlag={detail.value}"

        headers = {"consumerkey": self.key}
        response = self.session.get(url, header_auth=True, headers=headers)
        if response.status_code != 200:
            return None

        processed = json.loads(response.detail)
        return processed

    def order_stock(
        self,
        symbol: str,
        quantity: int,
        side,
        limit_price: float = None,
        price_type: PriceType = PriceType.MARKET,
        order_term: OrderTerm = OrderTerm.GOOD_UNTIL_CANCEL,
        market_session: MarketSession = MarketSession.REGULAR,
    ):
        preview_url = (
            _BASE_URL + "/v1/accounts/" + self.selected_account + "/orders/preview.json"
        )
        headers = {"Content-Type": "application/json", "consumerKey": self.key}

        client_order_id: int = random.randint(1000000000, 9999999999)

        preview_payload = {
            "PreviewOrderRequest": {
                "orderType": "EQ",
                "clientOrderId": client_order_id,
                "Order": [
                    {
                        "allOrNone": "false",
                        "priceType": price_type.value,
                        "orderTerm": order_term.value,
                        "marketSession": market_session.value,
                        "stopPrice": "",
                        "Instrument": [
                            {
                                "Product": {"securityType": "EQ", "symbol": symbol},
                                "orderAction": side.value,
                                "quantityType": "QUANTITY",
                                "quantity": quantity,
                            }
                        ],
                    }
                ],
            }
        }

        if limit_price is not None:
            preview_payload["PlaceOrderRequest"]["Order"]["limitPrice"] = limit_price

        response = self.session.post(
            preview_url,
            header_auth=True,
            headers=headers,
            data=json.dumps(preview_payload),
        )
        if response.status_code != 200:
            return False

        processed = json.loads(response.content)

        order_payload = {
            "PlaceOrderRequest": {
                "orderType": "EQ",
                "clientOrderId": client_order_id,
                "PreviewIds": [
                    {
                        "previewId": processed["PreviewOrderResponse"]["PreviewIds"][0][
                            "previewId"
                        ]
                    }
                ],
                "Order": [
                    {
                        "allOrNone": "false",
                        "priceType": price_type.value,
                        "orderTerm": order_term.value,
                        "marketSession": market_session.value,
                        "stopPrice": "",
                        "Instrument": [
                            {
                                "Product": {"securityType": "EQ", "symbol": symbol},
                                "orderAction": side.value,
                                "quantityType": "QUANTITY",
                                "quantity": quantity,
                            }
                        ],
                    }
                ],
            }
        }

        if limit_price is not None:
            order_payload["PlaceOrderRequest"]["Order"]["limitPrice"] = limit_price
        _BASE_URL = "https://api.etrade.com"
        order_url = f"{_BASE_URL}/v1/accounts/{self.selected_account}/orders/place.json"
        response = self.session.post(
            order_url, header_auth=True, headers=headers, data=json.dumps(order_payload)
        )
        if response.status_code != 200:
            return False

        processed = json.loads(response.content)

        return processed


    def order(self):
        pass

    def order_target(self):
        pass

    def order_target_portfolio(self):
        pass

    def account_value(self) -> float:
        params = {"instType": "BROKERAGE", "realTimeNAV": "true"}
        headers = {"consumerkey": self.key}

        url = f"{_BASE_URL}/v1/accounts/{self.selected_account}/balance.json"

        response = self.session.get(
            url, header_auth=True, params=params, headers=headers
        )

        if response.status_code != 200:
            return False

        resp = json.loads(response.content)

        return resp["BalanceResponse"]["Computed"]["RealTimeValues"]["totalAccountValue"]

    def send_order(self, new_order):
        order_response = self.session.place_order(account=self.session.accountId,
                                        order=new_order)
        order_id = order_response["order_id"]
        return order_response, order_id
    
    def cancel_order(self, order_id):
        return self.session.cancel_order(self.session.accountId, order_id)

    def get_order_info(self, order_id):  
        """
        order_status = 'REJECTED' | "FILLED" | "WORKING"
        """      
        order_info = self.session.get_orders(account=self.session.accountId,
                                              order_id=order_id)
        if order_info['orderStrategyType'] == "OCO":
            order_status = [
                order_info['childOrderStrategies'][0]['status'],
                order_info['childOrderStrategies'][1]['status']]
            if not order_status[0]==order_status[1]:
                print("OCO order status are different in ordID {order_id}: ",
                      f"{order_status[0]} vs {order_status[1]}")
            order_status = order_status[0]
        elif order_info['orderStrategyType'] in ['SINGLE', 'TRIGGER']:
            order_status = order_info['status']
        else:
            raise TypeError("Not sure type order. Check")
        return order_status, order_info

    def get_quotes(self, symbol:list):
        return self.session.get_quotes(instruments=symbol)

    def get_open_orders(self):
        pass

    def get_order_status(self, order_id):
        pass
    
    def get_account_info(self):
        acc_inf = self.session.get_accounts(self.session.accountId, ['orders','positions'])
        return acc_inf

    def get_positions_orders(self):
        acc_inf = self.get_account_info()

        df_pos = pd.DataFrame(columns=["symbol", "asset", "type", "Qty", "Avg Price", "PnL", "PnL %"])

        for pos in acc_inf['securitiesAccount']['positions']:
            long = True if pos["longQuantity"]>0 else False

            pos_inf = {
                "symbol":pos["instrument"]["symbol"],
                "asset":pos["instrument"]["assetType"],
                "type": "long" if  long else "short",
                "Avg Price": pos['averagePrice'],
                "PnL": pos["currentDayProfitLoss"],
                }
            pos_inf["Qty"] = int(pos[f"{pos_inf['type']}Quantity"])
            pos_inf["PnL %"] = pos_inf["PnL"]/(pos_inf["Avg Price"]*pos_inf["Qty"])
            df_pos =pd.concat([df_pos, pd.DataFrame.from_records(pos_inf, index=[0])], ignore_index=True)

        df_ordr = pd.DataFrame(columns=["symbol", "asset", "type", "Qty",
                                        "Price", "action"])
        return df_pos, df_ordr

    def make_BTO_lim_order(self, Symbol:str, Qty:int, price:float, strike=None, **kwarg):
        new_order=Order()
        new_order.order_strategy_type("TRIGGER")
        new_order.order_type("LIMIT")
        new_order.order_session('NORMAL')
        new_order.order_duration('GOOD_TILL_CANCEL')
        new_order.order_price(float(price))

        order_leg = OrderLeg()

        if strike is not None:
            order_leg.order_leg_instruction(instruction="BUY_TO_OPEN")
            order_leg.order_leg_asset(asset_type='OPTION', symbol=Symbol)
        else:
            order_leg.order_leg_instruction(instruction="BUY")
            order_leg.order_leg_asset(asset_type='EQUITY', symbol=Symbol)

        order_leg.order_leg_quantity(quantity=int(Qty))
        new_order.add_order_leg(order_leg=order_leg)
        return new_order


    def make_BTO_PT_SL_order(self, Symbol:str, Qty:int, price:float, PTs:list=None,
                            PTs_Qty:list=None, SL:float=None, SL_stop:float=None, **kwarg):
        new_order= self.make_BTO_lim_order(Symbol, Qty, price)

        if PTs == [None]:
            return new_order

        PTs_Qty = [ round(Qty * pqty) for pqty in PTs_Qty]
        for PT, pqty in zip(PTs, PTs_Qty):
            new_child_order = new_order.create_child_order_strategy()
            new_child_order = self.make_Lim_SL_order(Symbol, pqty, PT, SL, SL_stop, new_child_order)
            new_order.add_child_order_strategy(child_order_strategy=new_child_order)
        return new_order


    def make_Lim_SL_order(self, Symbol:str, Qty:int,  PT:float, SL:float, SL_stop:float=None, new_order=None, strike=None, **kwarg):
        if new_order is None:
            new_order = Order()
        new_order.order_strategy_type("OCO")

        child_order1 = new_order.create_child_order_strategy()
        child_order1.order_strategy_type("SINGLE")
        child_order1.order_type("LIMIT")
        child_order1.order_session('NORMAL')
        child_order1.order_duration('GOOD_TILL_CANCEL')
        child_order1.order_price(float(PT))

        child_order_leg = OrderLeg()

        child_order_leg.order_leg_quantity(quantity=Qty)
        if strike is not None:
            child_order_leg.order_leg_instruction(instruction="SELL_TO_CLOSE")
            child_order_leg.order_leg_asset(asset_type='OPTION', symbol=Symbol)
        else:
            child_order_leg.order_leg_instruction(instruction="SELL")
            child_order_leg.order_leg_asset(asset_type='EQUITY', symbol=Symbol)

        child_order1.add_order_leg(order_leg=child_order_leg)
        new_order.add_child_order_strategy(child_order_strategy=child_order1)

        child_order2 = new_order.create_child_order_strategy()
        child_order2.order_strategy_type("SINGLE")
        child_order2.order_session('NORMAL')
        child_order2.order_duration('GOOD_TILL_CANCEL')

        if SL_stop is not None:
            child_order2.order_type("STOP_LIMIT")
            child_order2.order_price(float(SL))
            child_order2.stop_price(float(SL_stop))
        else:
            child_order2.order_type("STOP")
            child_order2.stop_price(float(SL))

        child_order2.add_order_leg(order_leg=child_order_leg)
        new_order.add_child_order_strategy(child_order_strategy=child_order2)
        return new_order


    def make_STC_lim(self, Symbol:str, Qty:int, price:float, strike=None, **kwarg):
        new_order=Order()
        new_order.order_strategy_type("SINGLE")
        new_order.order_type("LIMIT")
        new_order.order_duration('GOOD_TILL_CANCEL')
        new_order.order_price(float(price))

        order_leg = OrderLeg()
        order_leg.order_leg_quantity(quantity=int(Qty))

        if strike is not None:
            new_order.order_session('NORMAL')
            order_leg.order_leg_instruction(instruction="SELL_TO_CLOSE")
            order_leg.order_leg_asset(asset_type='OPTION', symbol=Symbol)
        else:
            new_order.order_session('SEAMLESS')
            order_leg.order_leg_instruction(instruction="SELL")
            order_leg.order_leg_asset(asset_type='EQUITY', symbol=Symbol)
        new_order.add_order_leg(order_leg=order_leg)
        return new_order

    def make_STC_SL(self, Symbol:str, Qty:int, SL:float, strike=None,
                    SL_stop:float=None, new_order=Order(), **kwarg):
        new_order=Order()
        new_order.order_strategy_type("SINGLE")

        if SL_stop is not None:
            new_order.order_type("STOP_LIMIT")
            new_order.stop_price(float(SL_stop))
            new_order.order_price(float(SL))
        else:
            new_order.order_type("STOP")
            new_order.stop_price(float(SL))

        new_order.order_session('NORMAL')
        new_order.order_duration('GOOD_TILL_CANCEL')

        order_leg = OrderLeg()
        order_leg.order_leg_quantity(quantity=int(Qty))
        if strike is not None:
            order_leg.order_leg_instruction(instruction="SELL_TO_CLOSE")
            order_leg.order_leg_asset(asset_type='OPTION', symbol=Symbol)
        else:
            order_leg.order_leg_instruction(instruction="SELL")
            order_leg.order_leg_asset(asset_type='EQUITY', symbol=Symbol)
        new_order.add_order_leg(order_leg=order_leg)
        return new_order

    def make_STC_SL_trailstop(self, Symbol:str, Qty:int,  trail_stop_percent:float, new_order=None, strike=None, **kwarg):
        if new_order is None:
            new_order = Order()
        new_order.order_strategy_type("SINGLE")
        new_order.order_strategy_type("SINGLE")
        new_order.order_type("TRAILING_STOP")
        new_order.order_session('NORMAL')
        new_order.order_duration('GOOD_TILL_CANCEL')
        new_order.stop_price_offset(trail_stop_percent)
        new_order.stop_price_link_type('PERCENT')
        new_order.stop_price_link_basis('BID')
        
        child_order_leg = OrderLeg()
        child_order_leg.order_leg_quantity(quantity=Qty)
        if strike is not None:
            child_order_leg.order_leg_instruction(instruction="SELL_TO_CLOSE")
            child_order_leg.order_leg_asset(asset_type='OPTION', symbol=Symbol)
        else:
            child_order_leg.order_leg_instruction(instruction="SELL")
            child_order_leg.order_leg_asset(asset_type='EQUITY', symbol=Symbol)
        new_order.add_order_leg(order_leg=child_order_leg)
        return new_order







