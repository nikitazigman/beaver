package main

import (
	"encoding/json"
	"fmt"
	"strings"
)

type Foo struct {
	Foo string `json:"foo"`
	Boo bool   `json:"boo"`
}

func main() {
	body := `[{"foo": "asdf", "boo": true},{"foo": "f", "boo": true}]`
	reader := strings.NewReader(body)

	var foo []Foo
	decoder := json.NewDecoder(reader)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&foo)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(foo)

}
