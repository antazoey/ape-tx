# @version ^0.4.0

owner: public(address)
favorite_number: public(uint256)
previous_number: public(uint256)
friend: public(address)


event NumberChange:
    previous_number: uint256
    new_number: indexed(uint256)


event FriendChange:
    new_address: indexed(address)


@deploy
def __init__(owner: address):
    self.owner = owner


@external
def set_number(num: uint256):
    assert msg.sender == self.owner, "!authorized"
    assert num != 5
    self.previous_number = self.favorite_number
    self.favorite_number = num
    log NumberChange(self.previous_number, num)


@external
def set_address(_address: address):
    self.friend = _address
    log FriendChange(_address)
