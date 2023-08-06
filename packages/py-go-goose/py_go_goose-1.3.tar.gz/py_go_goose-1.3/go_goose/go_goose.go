package go_goose

import "github.com/Oneflow-Inc/go-goose"

var (
	g goose.Goose
)

func init() {
	g = goose.New()
}

func ExtractCleanText(rawHtml string) (results [2]string) {
	defer func() {
		a, err := g.ExtractFromRawHTML(rawHtml, "")
		if err == nil && a != nil {
			results = [2]string{a.CleanedText, a.Title}
		}
	}()

	return
}
