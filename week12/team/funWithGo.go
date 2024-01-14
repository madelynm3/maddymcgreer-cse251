package main

import "fmt"

func mainf() {
	fmt.Println("Hello, World!")

	var first string
	first = "This is the first string"
	fmt.Printf("first=%v \n", first)

	var second = 5
	fmt.Printf("second=%v \n", second)

	third := 3.14
	fmt.Printf("third=%v \n", third)

	fourth := new(int)
	fmt.Printf("fourth=%v \n", fourth)
	*fourth = 9
	fmt.Printf("fourth=%v \n", *fourth)

	fifth := make(map[string]int)
	fifth["k1"] = 7
	fifth["k2"] = 38
	fmt.Printf("fifth=%v \n", fifth)

	ch := make(chan int, 5)

}
