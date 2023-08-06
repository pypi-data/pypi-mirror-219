# Local
import openlimit.utilities as utils
from openlimit.buckets import Bucket, BucketReqTok


############
# BASE CLASS
############


class RateLimiter(object):
    def __init__(self, 
                 request_limit, 
                 token_limit, 
                 token_counter, 
                 resp_token_count, 
                 resources:list[str],
                 per_minutes=1,
                 verbose=False):
        
        if not resources:
            resources = ['default']
        
        # Token counter
        self.token_counter = token_counter
        self.response_token_count = resp_token_count

        # Buckets
        self.res_q = []
        self.res_bucket:dict[str, BucketReqTok] = {}
        index = 0
        for resource in resources:
            bks = BucketReqTok(verbose=verbose)
            bks.set_bucket(
                Bucket(id=index, unit='tok', rate_limit=token_limit, per_minutes=per_minutes, verbose=verbose),
                Bucket(id=index, unit='req', rate_limit=request_limit, per_minutes=per_minutes, verbose=verbose)
            )
            self.res_bucket[resource] = bks
            self.res_q.append(resource)
            index += 1

        self.cur_res = resources[0]


    async def wait_for_capacity(self, tokens_to_send):
        self.cur_res = self._get_available_or_first(tokens_to_send)
        bka = self._get_bucketsand(self.cur_res)
        await bka.wait_for_capacity(tokens_to_send)

    
    def limit(self, **kwargs):
        num_tokens = self.token_counter(kwargs['messages'])
        return utils.ContextManager(num_tokens, self)


    def is_limited(self):
        return utils.FunctionDecorator(self)
            

    def update(self, response):
        tok = self.response_token_count(response)
        bka = self._get_bucketsand(self.cur_res)
        bka.amount_confirmed(tok)
        return response


    def _get_bucketsand(self, resource) -> BucketReqTok|None:
        if resource in self.res_bucket:
            return self.res_bucket[resource]
        return None
    

    def _get_available_or_first(self, tokens_to_send):
        for res in self.res_q:
            bka = self._get_bucketsand(res)
            if bka._has_capacity(tokens_to_send):
                self.res_q.remove(res)
                self.res_q.append(res)
                return res
        return self.res_q[0]
    

######
# MAIN
######


class ChatRateLimiter(RateLimiter):
    def __init__(self, request_limit=3, token_limit=150000, resources=[], verbose=False):
        '''
        request_limit: number of requests per minute
        token_limit: number of tokens per minute
        '''
        super().__init__(
            request_limit=request_limit,
            token_limit=token_limit,
            token_counter=utils.num_tokens_consumed_by_chat_request,
            resp_token_count=utils.num_tokens_consumed_by_chat_response,
            resources=resources,
            verbose=verbose
        )


class EmbeddingRateLimiter(RateLimiter):
    def __init__(self, request_limit, token_limit, resources=1, verbose=False):
        '''
        request_limit: number of requests per minute
        token_limit: number of tokens per minute
        '''
        super().__init__(
            request_limit=request_limit, 
            token_limit=token_limit, 
            token_counter=utils.num_tokens_consumed_by_embedding_request,
            resp_token_count=utils.num_tokens_consumed_by_chat_response,
            resources=resources,
            verbose=verbose
        )