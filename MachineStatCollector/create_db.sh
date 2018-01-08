sudo su - postgres -c "psql -c \"create user stats_collector with password 'stats_collector' login;\""
sudo su - postgres -c "psql -c \"create database stats_collector with owner stats_collector;\""
sudo su - postgres -c "psql -c \"create user stats_collector_test with password 'stats_collector_test' login;\""
sudo su - postgres -c "psql -c \"create database stats_collector_test with owner stats_collector_test;\""