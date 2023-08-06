# Standard library
import asyncio
import datetime
import time


######
# MAIN
######


class Bucket(object):
    def __init__(self, id, unit, rate_limit, per_minutes=1, verbose=False):
        # once per x minutes
        self._rate_limit = rate_limit
        self._cap_seconds : int = per_minutes * 60
        self.verbose = verbose
        self.id = id
        self.unit = unit
        self._reset()
    
    def _reset(self):
        self._1st_sent_epoch = 0
        self._amount_sent = 0
        self._amount_sending = 0
        return True

    def _sec_passed(self):
        if self._1st_sent_epoch == 0:
            return 0
        cur_epoch = time.time()
        return cur_epoch - self._1st_sent_epoch
    
    def _log(self):
        if not self.verbose: return
        sec_passed = self._sec_passed()
        tnow =  datetime.datetime.fromtimestamp(time.time())
        now_m = tnow.minute
        now_s = tnow.second
        per_minu = self._rate_limit / (self._cap_seconds / 60)

        cur_time = f' {now_m:.0f}:{now_s:.0f} ({sec_passed:0.1f}s/{self._cap_seconds}s)'
        sent = f' sent: {self._amount_sent}/{int(per_minu)} {self.unit}'

        if self._amount_sending == 0:
            sending = ''
        else:
            sending = f', can send: {self._amount_sending} {self.unit}'

        print(f'[OpenLimit {self.id}]{cur_time}{sent}{sending}')


    def _is_period_past(self):
        sec_passed = self._sec_passed()
        if sec_passed > self._cap_seconds:
            return True
        return False
    
    def _has_capacity(self, amount_to_send):
        # if amount is larger than rate limit, can't do forever.
        if amount_to_send > self._rate_limit:
            False
        
        if self._is_period_past():
            return True

        amount_will_send_est = self._amount_sent + self._amount_sending + amount_to_send
        
        # rate is not exceeded. send.
        if amount_will_send_est <= self._rate_limit:
            return True
        
        return False
    
    def amount_confirmed(self, amount_sent):
        self._amount_sent += amount_sent
        self._amount_sending = 0

        self._log()

        # duration passed. reset.
        if self._is_period_past():
            self._reset()


    async def wait_for_capacity(self, amount_to_send):
        while not self._has_capacity(amount_to_send):
            sec_passed = self._sec_passed()
            sleep_sec = self._cap_seconds - sec_passed
            await asyncio.sleep(sleep_sec)

        if self._is_period_past():
            self._reset()

        self._amount_sending += amount_to_send
        if self._1st_sent_epoch == 0:
            self._1st_sent_epoch = time.time()
        
        self._log()


class BucketReqTok:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def set_bucket(self, bucket_tok:Bucket, bucket_req:Bucket):
        self.bucket_req = bucket_req
        self.bucket_tok = bucket_tok

    def amount_confirmed(self, amnt_tok, amnt_req=1):
        self.bucket_req.amount_confirmed(amnt_req)
        self.bucket_tok.amount_confirmed(amnt_tok)

    async def wait_for_capacity(self, amnt_to_send_tok, amnt_to_send_req=1):
        await asyncio.gather( 
            self.bucket_req.wait_for_capacity(amnt_to_send_req),
            self.bucket_tok.wait_for_capacity(amnt_to_send_tok)
        )

    def _has_capacity(self, amnt_to_send_tok, amnt_to_send_req=1):
        a = self.bucket_req._has_capacity(amnt_to_send_req)
        b = self.bucket_tok._has_capacity(amnt_to_send_tok)
        return a and b

