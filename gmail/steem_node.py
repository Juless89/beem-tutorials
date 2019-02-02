from beem import Steem
from beem.blockchain import Blockchain
from gmail import Gmail


class Steem_node():
    def __init__(self):
        self.stm = Steem()
        self.blockchain = Blockchain(
            steem_instance=self.stm,
            mode="head"
        )
        self.mailserver = Gmail(60)

    def run(self):
        # Fetch full blocks, then inspect each operation.
        for block in self.blockchain.blocks():
            block_num = block.block_num
            created_at = block.time()
            print(f'Block: {block_num}')

            for op in block.operations:
                # Extract op data
                if op['type'] == 'transfer_operation':
                    type = 'transfer'
                    subject = 'New transfer'
                    to = op['value']['to']
                    FROM = op['value']['from']
                    amount = op['value']['amount']
                    memo = op['value']['memo']

                    # Check if account matches, sent mail on True
                    if to == 'steempytutorials':
                        print('Incoming transfer')
                        message = (
                            f'{created_at}\nBlock: {block_num}\nFrom: {FROM}' +
                            f'\nTo: {to}\nAmount: {amount}\nMemo: {memo}\n'
                        )
                        try:
                            self.mailserver.send_email(subject, message, type)
                            print('Mail sent')
                        except Exception as e:
                            print('Failed to sent mail', e)


if __name__ == '__main__':
    steem_node = Steem_node()
    steem_node.run()
