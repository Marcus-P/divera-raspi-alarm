import importlib,os
def test_legacy_config_loads_and_gets_safe_defaults(tmp_path,monkeypatch):
 p=tmp_path/"config.toml"
 p.write_text("""[site]\nname="Altbestand"\n[routing]\ntest_mode=true\ntest_recipient_ids=[123]\n[weekly_test]\nenabled=true\nweekdays=["sunday"]\ntime="12:00"\n""")
 monkeypatch.setenv("DRA_CONFIG",str(p))
 import divera_alarm.settings as s
 importlib.reload(s);c=s.load_settings()
 assert c.site.name=="Altbestand"
 assert c.routing.test_mode is True
 assert c.routing.production_commissioned is False
 assert c.routing.technical_recipient_ids==[]
 assert c.monitoring.reboot_escalation_enabled is False
 s.save_settings(c)
 assert s.load_settings().site.name=="Altbestand"
