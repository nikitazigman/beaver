package loader

import (
	"fmt"
	"math/rand"
	"testing"
	"time"
)

func TestToEntities(t *testing.T) {
	input := []Script{
		{
			Title:         "title 1",
			Code:          "code",
			LinkToProject: "link",
			Language:      "language 1",
			Tags:          []string{"tag1", "tag2"},
			Contributors: []Contributor{
				{Name: "Name1", LastName: "LastName1", EmailAddress: "Email1"},
				{Name: "Name2", LastName: "LastName2", EmailAddress: "Email2"},
			},
		},
		{
			Title:         "title 2",
			Code:          "code",
			LinkToProject: "link",
			Language:      "language 2",
			Tags:          []string{"tag1", "tag3"},
			Contributors: []Contributor{
				{Name: "Name1", LastName: "LastName1", EmailAddress: "Email1"},
				{Name: "Name3", LastName: "LastName3", EmailAddress: "Email3"},
			},
		},
		{
			Title:         "title 3",
			Code:          "code",
			LinkToProject: "link",
			Language:      "language 2",
			Tags:          []string{"tag3"},
			Contributors: []Contributor{
				{Name: "Name2", LastName: "LastName2", EmailAddress: "Email2"},
			},
		},
	}
	result := toEntitiesToLoad(input, time.Now())

	// check number of create entities
	if len(result.UniqueScripts) != 3 {
		t.Errorf("Result should have 3 tag but got %d", len(result.UniqueScripts))
	}
	if len(result.UniqueTags) != 3 {
		t.Errorf("Result should have 3 tag but got %d", len(result.UniqueTags))
	}
	if len(result.UniqueContribs) != 3 {
		t.Errorf("Result should have 2 contributor but got %d", len(result.UniqueContribs))
	}
	if len(result.UniqueLangs) != 2 {
		t.Errorf("Result should have 2 lang but got %d", len(result.UniqueLangs))
	}

	// check scripts
	expScripts := map[string]struct {
		Title         string
		Code          string
		LinkToProject string
	}{
		"title 1": {
			Code:          "code",
			LinkToProject: "link",
		},
		"title 2": {
			Code:          "code",
			LinkToProject: "link",
		},
		"title 3": {
			Code:          "code",
			LinkToProject: "link",
		},
	}
	for _, s := range result.UniqueScripts {
		exp, exist := expScripts[s.title]
		if !exist {
			t.Errorf("script %s was not found", s.title)
		}
		if exp.Code != s.code {
			t.Errorf("exp code %s != res code %s", exp.Code, s.code)
		}
		if exp.LinkToProject != s.linkToProject {
			t.Errorf("exp link %s != res link %s", exp.LinkToProject, s.linkToProject)
		}
	}
	// check langs
	expLangs := map[string]struct{}{
		"language 2": {},
		"language 1": {},
	}
	for _, l := range result.UniqueLangs {
		if _, exist := expLangs[l]; !exist {
			t.Errorf("lang %s was not found", l)
		}
	}
	//check tags
	expTags := map[string]struct{}{
		"tag1": {},
		"tag2": {},
		"tag3": {},
	}
	for _, ut := range result.UniqueTags {
		if _, exist := expTags[ut]; !exist {
			t.Errorf("tag %s was not found", ut)
		}
	}
	// check contibs
	expContribs := map[string]struct {
		Name     string
		LastName string
	}{
		"Email1": {Name: "Name1", LastName: "LastName1"},
		"Email2": {Name: "Name2", LastName: "LastName2"},
		"Email3": {Name: "Name3", LastName: "LastName3"},
	}
	for _, c := range result.UniqueContribs {
		exp, exist := expContribs[c.EmailAddress]
		if !exist {
			t.Errorf("contrib %s was not found", c.EmailAddress)
		}
		if exp.Name != c.Name {
			t.Errorf("exp name %s != res name %s", exp.Name, c.Name)
		}
		if exp.LastName != c.LastName {
			t.Errorf("exp last name %s != res last name %s", exp.LastName, c.LastName)
		}
	}
}

func generateBenchmarkScripts(count int, contribPerScript int, tagsPerScript int) []Script {
	var scripts []Script
	tagPool := make([]string, 50)
	for i := range tagPool {
		tagPool[i] = fmt.Sprintf("tag%d", i+1)
	}
	langs := []string{"Go", "Python", "Rust", "JavaScript", "Java", "C++", "Ruby", "Swift", "TypeScript", "Kotlin"}

	for i := 0; i < count; i++ {
		var contributors []Contributor
		for j := 0; j < contribPerScript; j++ {
			contributors = append(contributors, Contributor{
				Name:         fmt.Sprintf("Name%d", i*10+j),
				LastName:     fmt.Sprintf("Last%d", i*10+j),
				EmailAddress: fmt.Sprintf("email%d@example.com", i*10+j),
			})
		}

		var tags []string
		for j := 0; j < tagsPerScript; j++ {
			tags = append(tags, tagPool[rand.Intn(len(tagPool))])
		}

		scripts = append(scripts, Script{
			Title:         fmt.Sprintf("title_%d", i),
			Code:          "// some code here",
			LinkToProject: fmt.Sprintf("https://github.com/project%d", i),
			Language:      langs[i%len(langs)],
			Tags:          tags,
			Contributors:  contributors,
		})
	}

	return scripts
}

func BenchmarkToEntities(b *testing.B) {
	input := generateBenchmarkScripts(100, 2, 3)
	time := time.Now()
	b.ResetTimer()
	for b.Loop() {
		toEntitiesToLoad(input, time)
	}
}
