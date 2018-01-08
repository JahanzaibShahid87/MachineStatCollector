Feature: Get stats from clients
	runner should get stats information from clients

	Scenario: All information should be collected.
		Given that client info 1, 192.168.1.104, 22, jahanzaib, mobile
		Then output should match
		Then All information of client should be popluated in database
		Then subject of email should match
		Then body should match for memory with type memory
		Then body should match for cpu with type cpu

