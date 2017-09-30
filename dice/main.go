package main

import (
	"fmt"
	"math/rand"
	"os"
	"time"
)

type attackDie struct {
	ranged int
	damage int
	surge  int
	miss   bool
}

type avgDie struct {
	ranged float64
	damage float64
	surge  float64
	miss   float64
}

// ATK
var blueDie = [6]attackDie{
	attackDie{0, 0, 0, true},
	attackDie{2, 2, 1, false},
	attackDie{3, 2, 0, false},
	attackDie{4, 2, 0, false},
	attackDie{5, 1, 0, false},
	attackDie{6, 1, 1, false}}
var redDie = [6]attackDie{
	attackDie{0, 1, 0, false},
	attackDie{0, 2, 0, false},
	attackDie{0, 2, 0, false},
	attackDie{0, 2, 0, false},
	attackDie{0, 3, 0, false},
	attackDie{0, 3, 1, false}}
var yellowDie = [6]attackDie{
	attackDie{1, 0, 1, false},
	attackDie{1, 1, 0, false},
	attackDie{2, 1, 0, false},
	attackDie{0, 1, 1, false},
	attackDie{0, 2, 0, false},
	attackDie{0, 2, 1, false}}
var greenDie = [6]attackDie{
	attackDie{0, 1, 0, false},
	attackDie{0, 0, 1, false},
	attackDie{1, 0, 1, false},
	attackDie{1, 1, 0, false},
	attackDie{0, 1, 1, false},
	attackDie{1, 1, 1, false}}

// DEF
var brownDie = [6]int{0, 0, 0, 1, 1, 2}
var grayDie = [6]int{0, 1, 1, 1, 2, 3}
var blackDie = [6]int{0, 2, 2, 2, 3, 4}

func rollBlue(r *rand.Rand) attackDie {
	return blueDie[r.Intn(6)]
}

func rollRed(r *rand.Rand) attackDie {
	return redDie[r.Intn(6)]
}

func rollYellow(r *rand.Rand) attackDie {
	return yellowDie[r.Intn(6)]
}

func rollGreen(r *rand.Rand) attackDie {
	return greenDie[r.Intn(6)]
}

func rollBrown(r *rand.Rand) int {
	return brownDie[r.Intn(6)]
}

func rollGray(r *rand.Rand) int {
	return grayDie[r.Intn(6)]
}

func rollBlack(r *rand.Rand) int {
	return blackDie[r.Intn(6)]
}

func usage() {
	panic("Usage: dice [--blue|--red|--yellow|--green|--brown|--grey|--black]")
}

func atkOrDef(verbose bool, defend bool, blue int, red int, yellow int, green int, brown int, gray int, black int) avgDie {
	r := rand.New(rand.NewSource(time.Now().UnixNano()))

	sum := attackDie{}
	min := attackDie{-1, -1, -1, false}
	max := attackDie{-1, -1, -1, false}
	count := 1000000000
	misses := 0
	minMisses := -1
	maxMisses := -1
	for i := 0; i < count; i++ {
		startingMisses := misses
		x := attackDie{}
		for j := 0; j < blue; j++ {
			y := rollBlue(r)
			if y.miss {
				misses++
				continue
			}
			x.damage += y.damage
			x.ranged += y.ranged
			x.surge += y.surge
		}
		for j := 0; j < red; j++ {
			y := rollRed(r)
			if y.miss {
				misses++
				continue
			}
			x.damage += y.damage
			x.ranged += y.ranged
			x.surge += y.surge
		}
		for j := 0; j < yellow; j++ {
			y := rollYellow(r)
			if y.miss {
				misses++
				continue
			}
			x.damage += y.damage
			x.ranged += y.ranged
			x.surge += y.surge
		}
		for j := 0; j < green; j++ {
			y := rollGreen(r)
			if y.miss {
				misses++
				continue
			}
			x.damage += y.damage
			x.ranged += y.ranged
			x.surge += y.surge
		}
		for j := 0; j < brown; j++ {
			x.damage += rollBrown(r)
		}
		for j := 0; j < gray; j++ {
			x.damage += rollGray(r)
		}
		for j := 0; j < black; j++ {
			x.damage += rollBlack(r)
		}
		sum.damage += x.damage
		sum.ranged += x.ranged
		sum.surge += x.surge
		if x.damage < min.damage || min.damage == -1 {
			min.damage = x.damage
		}
		if x.ranged < min.ranged || min.ranged == -1 {
			min.ranged = x.ranged
		}
		if x.surge < min.surge || min.surge == -1 {
			min.surge = x.surge
		}
		if x.damage > max.damage || max.damage == -1 {
			max.damage = x.damage
		}
		if x.ranged > max.ranged || max.ranged == -1 {
			max.ranged = x.ranged
		}
		if x.surge > max.surge || max.surge == -1 {
			max.surge = x.surge
		}
		xMisses := misses - startingMisses
		if xMisses < minMisses || minMisses == -1 {
			minMisses = xMisses
		}
		if xMisses > maxMisses || maxMisses == -1 {
			maxMisses = xMisses
		}
	}
	avgRanged := float64(sum.ranged) / float64(count)
	avgDamage := float64(sum.damage) / float64(count)
	avgSurge := float64(sum.surge) / float64(count)
	avgMiss := float64(misses) / float64(count)
	if defend {
		if verbose {
			fmt.Printf("%f (%d-%d)\n", avgDamage, min.damage, max.damage)
		}
		return avgDie{0, avgDamage, 0, 0}
	} else {
		if verbose {
			fmt.Printf("Damage: %f (%d-%d)\n", avgDamage, min.damage, max.damage)
			fmt.Printf(" Range: %f (%d-%d)\n", avgRanged, min.ranged, max.ranged)
			fmt.Printf("Surges: %f (%d-%d)\n", avgSurge, min.surge, max.surge)
			fmt.Printf("Misses: %f (%d-%d)\n", avgMiss, minMisses, maxMisses)
		}
		return avgDie{avgRanged, avgDamage, avgSurge, avgMiss}
	}
}

func atkAndDef(blue int, red int, yellow int, green int, brown int, gray int, black int) avgDie {
	atk := atkOrDef(false, true, blue, red, yellow, green, 0, 0, 0)
	def := atkOrDef(false, true, 0, 0, 0, 0, brown, gray, black)
	result := avgDie{
		atk.ranged - def.ranged,
		atk.damage - def.damage,
		atk.surge - def.surge,
		atk.miss - def.miss,
	}
	fmt.Printf("Damage: %f\n", result.damage)
	fmt.Printf(" Range: %f\n", result.ranged)
	fmt.Printf("Surges: %f\n", result.surge)
	fmt.Printf("Misses: %f\n", result.miss)
	return result
}

func main() {
	blue := 0
	red := 0
	yellow := 0
	green := 0
	brown := 0
	gray := 0
	black := 0
	for _, arg := range os.Args[1:] {
		if arg == "--blue" {
			blue++
		} else if arg == "--red" {
			red++
		} else if arg == "--yellow" {
			yellow++
		} else if arg == "--green" {
			green++
		} else if arg == "--brown" {
			brown++
		} else if arg == "--gray" || arg == "--grey" || arg == "--white" {
			gray++
		} else if arg == "--black" {
			black++
		} else {
			usage()
		}
	}

	attack := false
	defend := false
	if blue+red+yellow+green > 0 {
		attack = true
	}
	if brown+gray+black > 0 {
		defend = true
	}

	if attack && defend {
		atkAndDef(blue, red, yellow, green, brown, gray, black)
	} else if !attack && defend {
		atkOrDef(true, true, blue, red, yellow, green, brown, gray, black)
	} else if attack && !defend {
		atkOrDef(true, false, blue, red, yellow, green, brown, gray, black)
	} else {
		usage()
	}
}
