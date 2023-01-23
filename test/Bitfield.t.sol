// SPDX-License-Identifier: MIT
pragma solidity 0.8.16;

import "forge-std/Test.sol";
import "src/Bitfield.sol";

contract TestBitfields is Test {
    using Bitfields for Bitfields.Bitfield;

    Bitfields.Bitfield internal claims;
    Bitfields.Bitfield internal empty;

    function testBitFieldLib(
        uint8 _startEpoch,
        uint8 _leaveEpoch,
        uint8 _resumeEpoch
    ) public {
        vm.assume(_startEpoch < _leaveEpoch && _leaveEpoch <= _resumeEpoch);
        uint8 maxEpochs = type(uint8).max;

        claims = Bitfields.initialize(_startEpoch);

        for (uint8 epoch; epoch < maxEpochs; epoch++) {
            bool shouldBeActive = epoch >= _startEpoch;
            assertEq(claims.isActive(epoch), shouldBeActive);
        }

        claims.deactivateFrom(_leaveEpoch);

        for (uint8 epoch; epoch < maxEpochs; epoch++) {
            bool shouldBeActive = (epoch >= _startEpoch && epoch < _leaveEpoch);
            assertEq(claims.isActive(epoch), shouldBeActive);
            if (epoch >= _leaveEpoch)
                assertEq(claims.lastActive(epoch), _leaveEpoch - 1);
        }

        claims.activateFrom(_resumeEpoch);

        for (uint8 epoch; epoch < maxEpochs; epoch++) {
            bool shouldBeActive = ((epoch >= _startEpoch &&
                epoch < _leaveEpoch) || (epoch >= _resumeEpoch));
            assertEq(claims.isActive(epoch), shouldBeActive);
            if (epoch < _resumeEpoch && epoch >= _leaveEpoch)
                assertEq(claims.lastActive(epoch), _leaveEpoch - 1);
        }
    }
}
