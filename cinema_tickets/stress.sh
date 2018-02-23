#!/bin/sh
for i in 1..10; do
	flask stress_test --session 1a5e4465-3dd9-4137-ab88-1850a7a68618 &
done
