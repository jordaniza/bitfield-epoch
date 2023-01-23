# bitfield-epoch

A solidity library to efficiently compress user activations into a single 256 bit storage slot

# Why?

Solidity uses 8 bits as its smallest 'native' type, and working with these in arrays
is expensive. This library relies on some assumptions about epochs:

- Active users in epoch t are active in epochs t + k => k = 1...., K (unless they deactivate)
- Deactivated users in epoch t remain deactivated until they reactivate
- The user of this library has an awareness of the current epoch 4. Time moves strictly forward.

A bitfield is a 256 bit integer, indicating a user is active (1) or inactive (0) for epoch i.

Assuming a 1 month epoch, this allows us to store just over 21 years of activation history
in a single storage slot.

Initialize the array when activating the user for the first time, indicating what epoch they have
started from.

Activate or deactivate the user at specific epochs.

- Activating will set all subsequent epochs to active (1)
- Deactivating will set all subsequent epochs to inactive (0)

Check if a particular epoch is active or not using the `isActivated` function.

Finally, you can iterate back from the current epoch to check when was the last time the user
is activated.
Note: do not start from the last possible epoch (255) as 'activated' users will have all epochs by default
set to active (1). Instead, start from the current epoch.

# Setup

```sh
gh repo clone jordaniza/bitfield-epoch

forge build

# run tests:
forge test
```

See the test files for examples of use.
