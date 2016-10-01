from . import app, bot
from .utils import lookup_zodiac, lookup_chinese_zodiac
import requests


@bot.message_handler(regexp=r'^/about$')
def help(message):
    app.logger.debug("'about' command detected")
    about_text = (
        'BliJuga Bot v0.0.1\n\n'
        'For Hackathon purpose only'
    )
    bot.reply_to(message, about_text)
    #print(about_text)

@bot.message_handler(regexp=r'^/zodiac \d{4}\-\d{2}\-\d{2}$')
def zodiac(message):
    app.logger.debug("'zodiac' command detected")
    _, date_str = message.text.split(' ')
    _, month, day = parse_date(date_str)
    app.logger.debug('month = {}, day = {}'.format(month, day))

    try:
        zodiac = lookup_zodiac(month, day)
    except ValueError:
        bot.reply_to(message, 'Month or day is invalid')
    else:
        bot.reply_to(message, zodiac)


@bot.message_handler(regexp=r'^/shio \d{4}\-\d{2}\-\d{2}$')
def shio(message):
    app.logger.debug("'shio' command detected")
    _, date_str = message.text.split(' ')
    year, _, _ = parse_date(date_str)
    app.logger.debug('year = {}'.format(year))

    try:
        zodiac = lookup_chinese_zodiac(year)
    except ValueError:
        bot.reply_to(message, 'Year is invalid')
    else:
        bot.reply_to(message, zodiac)


    #@param nama, no hp, no akun bni
    #@proccess register akun telegram ke dalam apps
    #@output pesan berhasil/tidak no telp disimpan dalam database

@bot.message_handler(regexp=r'^/register .*$')
def register(message):
    app.logger.debug("'register' command detected")
    try:
        _, value = message.text.split('/register')
        processed = value[1:len(value)]
        namaold, password, nope = processed.split('-')
        nama = '_'.join(namaold.split(' '))
        idtel = message.chat.id
        r = requests.get('http://portfolio.hnymnky.com/register.php?username='+nama+'&password='+password+'&phone='+nope+'&id_telegram='+str(idtel))
        json_response = r.json()
        if(r.status_code == 200):
            if(json_response['statusId'] == 0):
                bot.reply_to(message,json_response['mesage'])
            else:
                bot.reply_to(message,'Akun '+namaold+' berhasil disimpan')
        else:
            bot.reply_to(message,"Terjadi kesalahan terhadap server, silahkan coba beberapa saat lagi")
    except ValueError:
        bot.reply_to(message,"Format Salah")
    #@param nama toko, alamat toko
    #@proccess register user sebagai merchan (bisa digunakan setelah terdaftar sebagai user)
    #@output pesan berhasil/tidak no telp disimpan dalam database

@bot.message_handler(regexp=r'^/mregister .*$')
def mregister(message):
    app.logger.debug("'mregister' command detected")
    try:
        _, value = message.text.split('/mregister')
        processed = value[1:len(value)]
        namatokoold, alamatold = processed.split('-')
        namatoko = '_'.join(namatokoold.split(' '))
        alamat = '_'.join(alamatold.split(' '))
        idtel = message.chat.id
        r = requests.get('http://portfolio.hnymnky.com/mregister.php?id_telegram='+str(idtel)+'&nama_toko='+namatoko+'&alamat='+alamat)
        json_response = r.json()
        if(r.status_code == 200):
            if(json_response['statusId'] == 0):
                bot.reply_to(message,json_response['mesage'])
            else:
                bot.reply_to(message,'Toko '+namatokoold+' berhasil disimpan')
        else:
            bot.reply_to(message,"Terjadi kesalahan terhadap server, silahkan coba beberapa saat lagi")
    except ValueError:
        bot.reply_to(message,"Format Salah")
    #@param masih belum tahu API BRI perlu apa aja
    #@proccess memeriksa saldo dari BRI ePay
    #@output pesan saldo

@bot.message_handler(regexp=r'^/balance$')
def balance(message):
    app.logger.debug("'ballance' command detected")
    idtel = message.chat.id
    r = requests.get('http://portfolio.hnymnky.com/balance.php?id_telegram='+str(idtel))
    json_response = r.json()
    if(r.status_code == 200):
        if(json_response['statusId'] == 0):
            bot.reply_to(message,json_response['mesage'])
        else:
            bot.reply_to(message,'Jumlah saldo dari BRI ePay anda adalah  '+json_response['result']['balance'])
    else:
        bot.reply_to(message,"Terjadi kesalahan terhadap server, silahkan coba beberapa saat lagi")
    #@param kode_promo, kode_transaksi
    #@proccess bergabung dengan room chat promo diadakan. 
    #          Terdapat validasi apakah balance mencukupi dan kode promo valid atau tidak
    #@output -

@bot.message_handler(regexp=r'^/transfer .*$')
def transfer(message):
    app.logger.debug("'transfer' command detected")
    try:
        _, value = message.text.split('/transfer')
        processed = value[1:len(value)]
        nope, jml = processed.split('-')
        idtel = message.chat.id
        r = requests.get('http://portfolio.hnymnky.com/transfer.php?id_telegram='+str(idtel)+'&phome='+nope+'&amount='+jml)
        json_response = r.json()
        if(r.status_code == 200):
            if(json_response['statusId'] == 0):
                bot.reply_to(message,json_response['mesage'])
            else:
                bot.reply_to(message,json_response['result'])
        else:
           bot.reply_to(message,"Terjadi kesalahan terhadap server, silahkan coba beberapa saat lagi")
    except ValueError:
        bot.reply_to(message,"Format Salah")
    #@param kode_transaksi
    #@proccess untuk memasukan token transaksi. Terdapat validasi apakah token valid atau tidak
    #@output pesan berhasil atau tidak

@bot.message_handler(regexp=r'^/join .*$')
def join(message):
    app.logger.debug("'join' command detected")
    try:
        _, value = message.text.split('/join')
        processed = value[1:len(value)]
        idpromo, jml = processed.split('-')
        idtel = message.chat.id
        r = requests.get('http://portfolio.hnymnky.com/join.php?id_telegram='+str(idtel)+'&id_promo='+idpromo+'&price='+jml)
        json_response = r.json()
        if(r.status_code == 200):
            if(json_response['statusId'] == 0):
                bot.reply_to(message,json_response['mesage'])
            else:
                bot.reply_to(message,json_response['result'])
        else:
            bot.reply_to(message,"Terjadi kesalahan terhadap server, silahkan coba beberapa saat lagi")
    except ValueError:
        bot.reply_to(message,"Format Salah")
    #@param kode room chat
    #@proccess untuk mengecheck status dari promo (masih berlaku atau tidak)
    #@output detail dari chat room promo tersebut

@bot.message_handler(regexp=r'^/status \w*$')
def status(message):
    app.logger.debug("'status' command detected")
    _, idprom = message.text.split(' ')
    r = requests.get('http://portfolio.hnymnky.com/status.php?id_promo='+idprom)
    json_response = r.json()
    if(r.status_code == 200):
        if(json_response['statusId'] == 0):
            bot.reply_to(message,json_response['mesage'])
        else:
            nama = 'Nama Promo '+json_response['result']['name']+'/n'
            startpro = 'Mulai Tanggal '+json_response['result']['start']+'/n'
            endpro = 'Berakhir Tanggal'+json_response['result']['end']+'/n'
            part = 'Jumlah Pelanggan '+'Berakhir Tanggal'+json_response['result']['participant']
            valueproc = nama+startpro+endpro+part
            bot.reply_to(message,valueproc)
    else:
        bot.reply_to(message,"Terjadi kesalahan terhadap server, silahkan coba beberapa saat lagi")
    #@param tanggal start, tanggal berakhir, judul promo, diskon(mungkin dalam persen) jumlah peserta, jumlah balance
    #@proccess untuk membuat promo dan chat room promo tersebut
    #@output detail dari chat room promo tersebut

@bot.message_handler(regexp=r'^/check_promo \w*$')
def check_promo(message):
    app.logger.debug("'check_promo' command detected")
    _, idprom = message.text.split(' ')
    r = requests.get('http://portfolio.hnymnky.com/addBalance.php?id_promo='+str(idprom))
    if(r.status_code == 200):
        r2 = requests.get('http://portfolio.hnymnky.com/announce.php?id_promo='+str(idprom))
        if(r2.status_code == 200):
            if(json_response['statusId'] == 0):
                bot.reply_to(message,json_response['mesage'])
            else:
                valueproc = json_response['result']
                for user in valueproc:
                    bot.send_message(int(user), "Selamat anda mendapat diskon dari id promo "+idprom)
        else:
            bot.reply_to(message,"Terjadi kesalahan terhadap server, silahkan coba beberapa saat lagi")    
    else:
        bot.reply_to(message,"Terjadi kesalahan terhadap server, silahkan coba beberapa saat lagi")
    #@param jumlah transaksi
    #@proccess untuk membuat kode transaksi
    #@output kode transaksi kalau berhasil , pesan kalau gagal

@bot.message_handler(regexp=r'^/bill \w$')
def bill(message):
    app.logger.debug("'bill' command detected")


    #Tambahan fungsi notifikasi, kayaknya sulit kalaujadi method 
    #@param jumlah transaksi
    #@proccess untuk membuat kode transaksi
    #@output kode transaksi kalau berhasil , pesan kalau gagal


def parse_date(text):
    return tuple(map(int, text.split('-')))
