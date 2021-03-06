irc-rabbitmq
============

IRC Program Using RabbitMQ Server
	
**Cara menjalankan program**
	Eksekusi program gunakan perintah `python RabbitMQClient.py`
	
**Daftar tes**
	**uji perintah /NICK tanpa parameter**
	1. jalankan perintah `/NICK` pada terminal
	2. program akan memberi output: `Generated random nickname: 027-XXXXX`, dimana X adalah karakter random
	
	**uji perintah /JOIN dengan parameter channel**
	1. jalankan perintah `/JOIN 027` pada terminal
	2. program akan memberi output:
		`Successfully join to channel 027`
		`Waiting for channel 027`
	
	**uji mengirim pesan ke channel spesifik**
	1. misalnya jalankan perintah `@027 hello folks !`
	2. program ini akan memberi output:
		`sent to channel 027`
		`[027] (027-XXXXX) hello folks !`
	3. program lain yang join channel `027` akan mendapat output:
		`[027] (027-XXXXX) hello folks !`
	
	**uji mengirim pesan broadcast**
	1. misalnya jalankan perintah `hello this is broadcast message`
	2. program ini akan memberi output:
		`[027] (027-d9rBY)  hello this is broadcast message`
		`[027a] (027-d9rBY)  hello this is broadcast message`
		`Successfully sent to all joined channel`
	3. program lain yang join channel `027` akan mendapat output:
		`[027] (027-d9rBY)  hello this is broadcast message`
	4. program lain yang join channel `027a` akan mendapat output:
		`[027a] (027-d9rBY)  hello this is broadcast message`
		
	**uji meninggalkan channel**
	1. jalankan perintah `/LEAVE 027` pada terminal
	2. program ini akan memberi output:
		`Successfully left channel 027`
	3. program lain tidak akan menerima output apapun
	
	**uji keluar dari program**
	1. jalankan perintah `/EXIT` pada terminal
	2. program ini akan memberi output:
		`[027a] (027-d9rBY) left channel`
		`[027] (027-d9rBY) left channel`
		`program closed`
	3. program lain yang join channel `027` akan mendapat output:
		`[027] (027-d9rBY) left channel`
	4. program lain yang join channel `027a` akan mendapat output:
		`[027a] (027-d9rBY) left channel`

