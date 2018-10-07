wrk.method = "POST"
wrk.body   = '[{"dst": "2.2.2.2", "protocol": "17", "active": "1", "comment": "{\\"comment\\":\\"Host DNS limit\\"}", "target": "ACCEPT", "direction": "EGRESS", "sport": "50", "fqdn": "nest0.gwa.demo.", "src": "1.1.2.1", "type": "FIREWALL_ADMIN", "priority": "10", "dport": "50", "raw_data": "{\\"hashlimit\\":\\"1001\\"}"}]'
wrk.headers["Content-Type"] = "application/x-www-form-urlencoded"



-- Below is the command:
-- wrk -c1 -t1 -d1s -s post.lua http://127.0.0.1:80/API/host_policy/Firewall
-- wrk -c1 -t1 -d1s -s post.lua http://127.0.0.1:80/testing
