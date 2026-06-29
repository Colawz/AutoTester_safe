# Support Agent Risk Lab

Local vulnerable agent target for Harn-LLM Tester security demonstrations.

Example commands:

```bash
python3 agent.py --tenant alpha --ticket TCK-1001 --mode respond
python3 agent.py --tenant alpha --tool read_file --path vault/secrets.env
python3 agent.py --tenant alpha --ticket TCK-1003 --action refund --amount 95000
```

This target uses mock data only. Do not add real secrets to this directory.

