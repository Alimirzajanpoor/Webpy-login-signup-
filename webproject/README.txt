login with webpy PROJECT:
project config:
	baraye run kardane proje va test bayad database sqlite ro dashte bashin ba dar dir khode proje yek file sqlite gozashte bashin
	
	man baraye display kardane aks capctha az webserver NGIX (aval bayad webserver ro run konid) estefade kardam va age project/templates/ berin file src tage img "http://localhost/image/kek.png" 
	(albate aval bayad congif NGIX anjam bedin ke dar payin in file text migam)

	bade inke file db sakhtin bayad berid to making_table.py (age avalin bare darin in proje ro systemeton run mikonid) ta table haye morede nazaro ba estefade az excute kardan func ha
	besazin.
	to file main.py db_url ham havaseton bashe ke url eshtebah nadin.
NGIX config:
	bade download NGIX bayad berin to nginx-1.22.1\conf\nginx.cong 
	va to bakhsh server to ghesmate root dir folder statics ke to proje
	hast ro bedin
	bade dadan dir mitonin NGIX ro run konid va bad projero run konid


