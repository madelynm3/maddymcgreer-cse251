/*
	---------------------------------------

Course: CSE 251
Lesson Week: 12
File: team.go
Author: Brother Comeau

Purpose: team activity - finding primes

Instructions:

- Process the array of numbers, find the prime numbers using goroutines

worker()

This goroutine will take in a list/array/channel of numbers.  It will place
prime numbers on another channel

readValue()

This goroutine will display the contents of the channel containing
the prime numbers

---------------------------------------
*/
package main

import (
	"fmt"
	"sync"
	"time"
)

var globalNumberOfPrimes = 0

func isPrime(n int) bool {
	// Primality test using 6k+-1 optimization.
	// From: https://en.wikipedia.org/wiki/Primality_test

	if n <= 3 {
		return n > 1
	}

	if n%2 == 0 || n%3 == 0 {
		return false
	}

	i := 5
	for (i * i) <= n {
		if n%i == 0 || n%(i+2) == 0 {
			return false
		}
		i += 6
	}
	return true
}

func worker(id int, numbers chan int, primes chan int, wg *sync.WaitGroup) {
	for num := range numbers {
		if isPrime(num) {
			primes <- num
		}

		wg.Done()
	}
}

func readValues(primes chan int) int {
	total := 0
	for range primes {
		total += 1
	}
	return total
}

func main() {
	startTime := time.Now()

	workers := 10
	numberValues := 110_003
	start := 10_000_000_000

	// Create any channels that you need
	numbers := make(chan int, numberValues)
	primes := make(chan int, numberValues)

	// Create any other "things" that you need to get the workers to finish(join)
	wg := new(sync.WaitGroup)

	// create workers
	for w := 1; w <= workers; w++ {
		go worker(w, numbers, primes, wg) // Add any arguments
	}

	for i := start; i < start+numberValues; i++ {
		wg.Add(1)
		numbers <- i
	}

	wg.Wait()

	close(numbers)
	close(primes)

	total := readValues(primes)

	elapsed := time.Since(startTime)
	fmt.Printf("Found %v primes in %v", total, elapsed)

}
