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

type rangedDie struct {
	avg avgDie
	min avgDie
	max avgDie
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

// ATK
var blueDieResult = rangedDie{
	avgDie{float64(10) / 3, float64(4) / 3, float64(1) / 3, float64(1) / 6},
	avgDie{0, 0, 0, 0},
	avgDie{2, 6, 1, 1},
}
var redDieResult = rangedDie{
	avgDie{0, float64(13) / 6, float64(1) / 6, 0},
	avgDie{0, 1, 0, 0},
	avgDie{0, 3, 1, 0},
}
var yellowDieResult = rangedDie{
	avgDie{float64(10) / 3, float64(4) / 3, float64(1) / 3, float64(1) / 6},
	avgDie{float64(2) / 3, float64(7) / 6, float64(1) / 2, 0},
	avgDie{2, 2, 1, 0},
}
var greenDieResult = rangedDie{
	avgDie{float64(1) / 2, float64(2) / 3, float64(2) / 3, 0},
	avgDie{0, 0, 0, 0},
	avgDie{1, 1, 1, 0},
}

// DEF
var brownDieResult = rangedDie{
	avgDie{0, float64(-2) / 3, 0, 0},
	avgDie{0, -2, 0, 0},
	avgDie{0, 0, 0, 0},
}
var grayDieResult = rangedDie{
	avgDie{0, float64(-4) / 3, 0, 0},
	avgDie{0, -3, 0, 0},
	avgDie{0, 0, 0, 0},
}
var blackDieResult = rangedDie{
	avgDie{0, float64(-13) / 6, 0, 0},
	avgDie{0, -4, 0, 0},
	avgDie{0, 0, 0, 0},
}

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
	panic("Usage: dice [--blue|--red|--yellow|--green|--brown|--grey|--black|--sim]")
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
			fmt.Printf("%f (%d -> %d)\n", avgDamage, min.damage, max.damage)
		}
		return avgDie{0, avgDamage, 0, 0}
	} else {
		if verbose {
			fmt.Printf("Damage: %.2f (%d -> %d)\n", avgDamage, min.damage, max.damage)
			fmt.Printf(" Range: %.2f (%d -> %d)\n", avgRanged, min.ranged, max.ranged)
			fmt.Printf("Surges: %.2f (%d -> %d)\n", avgSurge, min.surge, max.surge)
			fmt.Printf("Misses: %.2f (%d -> %d)\n", avgMiss, minMisses, maxMisses)
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

func nonSim(verbose bool, iblue int, ired int, iyellow int, igreen int, ibrown int, igray int, iblack int) avgDie {
	blue := float64(iblue)
	red := float64(ired)
	yellow := float64(iyellow)
	green := float64(igreen)
	brown := float64(ibrown)
	gray := float64(igray)
	black := float64(iblack)

	attack := false
	if blue+red+yellow+green > 0 {
		attack = true
	}

	avg := avgDie{0, 0, 0, 0}
	min := avgDie{0, 0, 0, 0}
	max := avgDie{0, 0, 0, 0}

	avg.damage = blue*blueDieResult.avg.damage + red*redDieResult.avg.damage +
		yellow*yellowDieResult.avg.damage + green*greenDieResult.avg.damage +
		(brown*brownDieResult.avg.damage + gray*grayDieResult.avg.damage + black*blackDieResult.avg.damage)
	avg.ranged = blue*blueDieResult.avg.ranged + red*redDieResult.avg.ranged +
		yellow*yellowDieResult.avg.ranged + green*greenDieResult.avg.ranged
	avg.surge = blue*blueDieResult.avg.surge + red*redDieResult.avg.surge +
		yellow*yellowDieResult.avg.surge + green*greenDieResult.avg.surge
	avg.miss = blue*blueDieResult.avg.miss + red*redDieResult.avg.miss +
		yellow*yellowDieResult.avg.miss + green*greenDieResult.avg.miss

	min.damage = blue*blueDieResult.min.damage + red*redDieResult.min.damage +
		yellow*yellowDieResult.min.damage + green*greenDieResult.min.damage +
		(brown*brownDieResult.min.damage + gray*grayDieResult.min.damage + black*blackDieResult.min.damage)
	min.ranged = blue*blueDieResult.min.ranged + red*redDieResult.min.ranged +
		yellow*yellowDieResult.min.ranged + green*greenDieResult.min.ranged
	min.surge = blue*blueDieResult.min.surge + red*redDieResult.min.surge +
		yellow*yellowDieResult.min.surge + green*greenDieResult.min.surge
	min.miss = blue*blueDieResult.min.miss + red*redDieResult.min.miss +
		yellow*yellowDieResult.min.miss + green*greenDieResult.min.miss

	max.damage = blue*blueDieResult.max.damage + red*redDieResult.max.damage +
		yellow*yellowDieResult.max.damage + green*greenDieResult.max.damage +
		(brown*brownDieResult.max.damage + gray*grayDieResult.max.damage + black*blackDieResult.max.damage)
	max.ranged = blue*blueDieResult.max.ranged + red*redDieResult.max.ranged +
		yellow*yellowDieResult.max.ranged + green*greenDieResult.max.ranged
	max.surge = blue*blueDieResult.max.surge + red*redDieResult.max.surge +
		yellow*yellowDieResult.max.surge + green*greenDieResult.max.surge
	max.miss = blue*blueDieResult.max.miss + red*redDieResult.max.miss +
		yellow*yellowDieResult.max.miss + green*greenDieResult.max.miss

	if verbose {
		if attack {
			fmt.Printf("Damage: %.2f (%d -> %d)\n", avg.damage, int(min.damage), int(max.damage))
			fmt.Printf(" Range: %.2f (%d -> %d)\n", avg.ranged, int(min.ranged), int(max.ranged))
			fmt.Printf("Surges: %.2f (%d -> %d)\n", avg.surge, int(min.surge), int(max.surge))
			fmt.Printf("Misses: %.2f (%d -> %d)\n", avg.miss, int(min.miss), int(max.miss))
		} else {
			fmt.Printf("%.2f (%d -> %d)\n", avg.damage, int(min.damage), int(max.damage))
		}
	}
	return avgDie{}
}

func main() {
	sim := false
	blue := 0
	red := 0
	yellow := 0
	green := 0
	brown := 0
	gray := 0
	black := 0
	for _, arg := range os.Args[1:] {
		if arg == "--sim" {
			sim = true
		} else if arg == "--blue" {
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

	if !sim {
		nonSim(true, blue, red, yellow, green, brown, gray, black)
	} else if attack && defend {
		atkAndDef(blue, red, yellow, green, brown, gray, black)
	} else if !attack && defend {
		atkOrDef(true, true, blue, red, yellow, green, brown, gray, black)
	} else if attack && !defend {
		atkOrDef(true, false, blue, red, yellow, green, brown, gray, black)
	} else {
		usage()
	}
}
