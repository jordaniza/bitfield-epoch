"""
Not essential but explains a bit better how binary operations can work
As solidity doesn't make it super easy to view binary values.

Just run this with `python bitfields.py` to look at the logs, we replicate this kind
of logic in the MerkleDistributor and in the StakingRewards
"""


# print decimal in binary in little endian with leading zeros
def bprint(input: int, desc: str = ""):
    return print(format(input, f"#0{size + 2}b"), f"       {desc}")

# bitmask is just all binary values flipped to "on" up to a certain point
def bitmask(len: int):
    return (1 << len) - 1


size = 32                                                       # in solidity we use 256bits, but 32 makes for nicer logs
empty_slot = 0
full_slot = bitmask(size)                                       # Initialize a full storage slot. You can't do this with uint8 in solidity b/c overflow

bprint(empty_slot, "EMPTY ARRAY")
bprint(full_slot, "FULL ARRAY")

start_epoch = 5                                                 # user starts at epoch 5
offset = bitmask(start_epoch)                                   # bitmask for first 5 epochs
bprint(offset, f"FIRST {start_epoch} OFFSET")

claims = offset ^ full_slot                                     # xor with the bitmask yields 0 for the first 5 bits
bprint(claims, f"IGNORING FIRST {start_epoch} CLAIMS")          # all epochs set to 1 from epoch 5 onwards

epoch_offline = 10                                              # user leaves at epoch 10
mask = bitmask(epoch_offline)                                   # next bitmask at epoch 10 will prevent overwriting existing data (1st 10 epochs)
claims = (mask & claims)                                        # bitwise AND will put all subsequent claims past epoch 10 back to zero
bprint(claims, f"OFFLINE FROM EPOCH {epoch_offline}")

epoch_back = 15                                                 # user comes back at epoch 15
bitmask_turn_on = bitmask(epoch_back)                           # this bitmask will prevent overwriting data before epoch 15
resume = bitmask_turn_on ^ full_slot                            # creates 1's for all bits 15th and above
bprint(resume, "RESUME XOR")

claims = resume ^ claims
bprint(claims, "RESUME FROM EPOCH 15")                          # xor with the bitmask to return the original data for 1st 15 bits