#!/usr/bin/env bats

FROM=$1
TO=$2

if [ -z "$FROM" ]; then
    FROM="demo@example.org"
fi

if [ -z "$TO" ]; then
    TO="test@gmail.com"
fi

# Wait for postfix to startup
wait-for-service -q tcp://postfix_test_587:587

SMTP_DATA="-smtp postfix_test_587 -port 587"

@test "Make sure postfix rejects the message from us" {
	! mailsend \
		-sub "Test email 1" $SMTP_DATA \
			-from "$FROM" -to "$TO" \
		body \
			-msg "Hello world!\nThis is a simple test message!"
}
