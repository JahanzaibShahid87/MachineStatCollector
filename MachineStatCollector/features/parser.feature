Feature: Parse XML
	parser should hanlde possible correct responses of parser.

	Scenario: All tag's value should matched.
		Given that parse the correct config file config_test.xml
		Then all parameters should match
		Then database should populate data
