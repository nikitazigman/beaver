package loader

import (
	"beaver-api/internal/business/contributor"
	"beaver-api/internal/business/language"
	"beaver-api/internal/business/script"
	"beaver-api/internal/business/tag"
	"reflect"
	"sort"
	"testing"
	"time"

	"github.com/google/uuid"
)

func TestToEntities(t *testing.T) {
	input := []ScriptDetail{
		{
			Title:         "title 1",
			Code:          "code",
			LinkToProject: "link",
			Language:      Language{Name: "language 1"},
			Tags:          []Tag{{Name: "tag1"}, {Name: "tag1"}},
			Contributors: []Contributor{
				{Name: "Name", LastName: "LastName", EmailAddress: "Email1"},
				{Name: "Name", LastName: "LastName", EmailAddress: "Email2"},
			},
		},
		{
			Title:         "title 2",
			Code:          "code 2 ",
			LinkToProject: "link 3",
			Language:      Language{Name: "language 1"},
			Tags:          []Tag{{Name: "tag1"}, {Name: "tag2"}},
			Contributors: []Contributor{
				{Name: "Name", LastName: "ContrLast", EmailAddress: "Email1"},
			},
		},
		{
			Title:         "title 3",
			Code:          "code 3",
			LinkToProject: "link 3",
			Language:      Language{Name: "language 2"},
			Tags:          []Tag{{Name: "tag1"}, {Name: "tag3"}},
			Contributors: []Contributor{
				{Name: "Name", LastName: "ContrLast", EmailAddress: "Email2"},
			},
		},
	}
	result := toEntities(input, time.Now())

	// check number of create entities
	if len(result.scripts) != 3 {
		t.Errorf("Result should have 3 tag but got %d", len(result.scripts))
	}
	if len(result.tags) != 3 {
		t.Errorf("Result should have 3 tag but got %d", len(result.tags))
	}
	if len(result.contributors) != 2 {
		t.Errorf("Result should have 2 contributor but got %d", len(result.contributors))
	}
	if len(result.langs) != 2 {
		t.Errorf("Result should have 2 lang but got %d", len(result.langs))
	}
	if len(result.tagScript) != 6 {
		t.Errorf("Result should have 6 tagScript link but got %d", len(result.tagScript))
	}
	if len(result.contribScript) != 4 {
		t.Errorf("Result should have 4 contribScript link but got %d", len(result.contribScript))
	}

	// check FK and m2m correctness

	// create helper mapping
	sm := make(map[string]script.Script)
	for _, s := range result.scripts {
		sm[s.Title] = s
	}
	lm := make(map[string]language.Language)
	for _, l := range result.langs {
		lm[l.Name] = l
	}
	tm := make(map[string]tag.Tag)
	for _, t := range result.tags {
		tm[t.Name] = t
	}
	cm := make(map[string]contributor.Contributor)
	for _, c := range result.contributors {
		cm[c.EmailAddress] = c
	}
	tsm := make(map[uuid.UUID][]uuid.UUID)
	for _, ts := range result.tagScript {
		tsm[ts.ScriptID] = append(tsm[ts.ScriptID], ts.TagID)
	}
	csm := make(map[uuid.UUID][]uuid.UUID)
	for _, cs := range result.contribScript {
		csm[cs.ScriptID] = append(csm[cs.ScriptID], cs.ContributorID)
	}

	// check correctness for each script
	for _, n := range input {
		s, ok := sm[n.Title]
		if !ok {
			t.Fatalf("Cannot find related script %s", n.Title)
		}
		l, ok := lm[n.Language.Name]
		if !ok {
			t.Fatalf("Cannot find related lang %s for script %s", n.Language.Name, n.Title)
		}
		// check script has correct language ID
		if s.LanguageID != l.ID {
			t.Errorf("Script %s has incorrect language id", n.Title)
		}

		// check script has correct links to the tags
		ts, ok := tsm[s.ID]
		if !ok {
			t.Fatalf("Cannot find related tags for script %s", n.Title)
		}
		sort.Slice(ts, func(i, j int) bool { return ts[i].String() < ts[j].String() })

		tIDs := make([]uuid.UUID, len(n.Tags))
		for i, tg := range n.Tags {
			tr, ok := tm[tg.Name]
			if !ok {
				t.Fatalf("Cannot find related tag %s for script %s", tg.Name, n.Title)
			}
			tIDs[i] = tr.ID
		}
		sort.Slice(tIDs, func(i, j int) bool { return tIDs[i].String() < tIDs[j].String() })
		if !reflect.DeepEqual(tIDs, ts) {
			t.Errorf("Script %s has incorrect tag assignment. Expected %s got %s", n.Title, tIDs, ts)
		}

		// check script has correct links to contributors
		cs, ok := csm[s.ID]
		if !ok {
			t.Fatalf("Cannot find related contributors for script %s", n.Title)
		}
		sort.Slice(cs, func(i, j int) bool { return cs[i].String() < cs[j].String() })

		cIDs := make([]uuid.UUID, len(n.Contributors))
		for i, c := range n.Contributors {
			cr, ok := cm[c.EmailAddress]
			if !ok {
				t.Fatalf("Cannot find related contributor %s for script %s", c.Name, n.Title)
			}
			cIDs[i] = cr.ID
		}
		sort.Slice(cIDs, func(i, j int) bool { return cIDs[i].String() < cIDs[j].String() })
		if !reflect.DeepEqual(cIDs, cs) {
			t.Errorf("Script %s has incorrect contributor assignment. Expected %s got %s", n.Title, cIDs, cs)
		}
	}
}

func BenchmarkToEntities(b *testing.B) {
	input := []ScriptDetail{
		{
			Title:         "title 1",
			Code:          "code",
			LinkToProject: "link",
			Language:      Language{Name: "language 1"},
			Tags:          []Tag{{Name: "tag1"}, {Name: "tag1"}},
			Contributors: []Contributor{
				{Name: "Name", LastName: "LastName", EmailAddress: "Email1"},
				{Name: "Name", LastName: "LastName", EmailAddress: "Email2"},
			},
		},
		{
			Title:         "title 2",
			Code:          "code 2 ",
			LinkToProject: "link 3",
			Language:      Language{Name: "language 1"},
			Tags:          []Tag{{Name: "tag1"}, {Name: "tag2"}},
			Contributors: []Contributor{
				{Name: "Name", LastName: "ContrLast", EmailAddress: "Email1"},
			},
		},
		{
			Title:         "title 3",
			Code:          "code 3",
			LinkToProject: "link 3",
			Language:      Language{Name: "language 2"},
			Tags:          []Tag{{Name: "tag1"}, {Name: "tag3"}},
			Contributors: []Contributor{
				{Name: "Name", LastName: "ContrLast", EmailAddress: "Email2"},
			},
		},
		{
			Title:         "title 4",
			Code:          "code 3",
			LinkToProject: "link 3",
			Language:      Language{Name: "language 2"},
			Tags:          []Tag{{Name: "tag1"}, {Name: "tag3"}},
			Contributors: []Contributor{
				{Name: "Name", LastName: "ContrLast", EmailAddress: "Email2"},
			},
		},
		{
			Title:         "title 5",
			Code:          "code 3",
			LinkToProject: "link 3",
			Language:      Language{Name: "language 2"},
			Tags:          []Tag{{Name: "tag1"}, {Name: "tag4"}},
			Contributors: []Contributor{
				{Name: "Name", LastName: "ContrLast", EmailAddress: "Email1"},
			},
		},
		{
			Title:         "title 6",
			Code:          "code 3",
			LinkToProject: "link 3",
			Language:      Language{Name: "language 2"},
			Tags:          []Tag{{Name: "tag2"}, {Name: "tag3"}},
			Contributors: []Contributor{
				{Name: "Name", LastName: "ContrLast", EmailAddress: "Email3"},
			},
		},
		{
			Title:         "title 7",
			Code:          "code 3",
			LinkToProject: "link 3",
			Language:      Language{Name: "language 2"},
			Tags:          []Tag{{Name: "tag2"}, {Name: "tag3"}},
			Contributors: []Contributor{
				{Name: "Name", LastName: "ContrLast", EmailAddress: "Email3"},
			},
		},
		{
			Title:         "title 8",
			Code:          "code 3",
			LinkToProject: "link 3",
			Language:      Language{Name: "language 3"},
			Tags:          []Tag{{Name: "tag2"}, {Name: "tag3"}},
			Contributors: []Contributor{
				{Name: "Name", LastName: "ContrLast", EmailAddress: "Email3"},
			},
		},
		{
			Title:         "title 9",
			Code:          "code 3",
			LinkToProject: "link 3",
			Language:      Language{Name: "language 1"},
			Tags:          []Tag{{Name: "tag2"}, {Name: "tag3"}},
			Contributors: []Contributor{
				{Name: "Name", LastName: "ContrLast", EmailAddress: "Email3"},
			},
		},
		{
			Title:         "title 10",
			Code:          "code 3",
			LinkToProject: "link 3",
			Language:      Language{Name: "language 1"},
			Tags:          []Tag{{Name: "tag1"}, {Name: "tag4"}},
			Contributors: []Contributor{
				{Name: "Name", LastName: "ContrLast", EmailAddress: "Email3"},
			},
		},
	}
	time := time.Now()
	for b.Loop() {
		toEntities(input, time)
	}
}
