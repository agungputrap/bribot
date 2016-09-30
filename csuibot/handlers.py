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
    #@param nama toko, alamat toko
    #@proccess register user sebagai merchan (bisa digunakan setelah terdaftar sebagai user)
    #@output pesan berhasil/tidak no telp disimpan dalam database

@bot.message_handler(regexp=r'^/mregister .*$')
def mregister(message):
    app.logger.debug("'mregister' command detected")
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
    #@param masih belum tahu API BRI perlu apa aja
    #@proccess memeriksa saldo dari BRI ePay
    #@output pesan saldo

@bot.message_handler(regexp=r'^/ballance$')
def ballance(message):
    app.logger.debug("'mregister' command detected")
    idtel = message.chat.id
    r = requests.get('http://portfolio.hnymnky.com/balance.php?id_telegram='+str(idtel))
    if(r.status_code == 200):
        if(json_response['statusId'] == 0):
            bot.reply_to(message,json_response['mesage'])
        else:
            bot.reply_to(message,'Jumlah saldo dari BRI ePay anda adalah  '+json_response['mesage'])
    else:
        bot.reply_to(message,"Terjadi kesalahan terhadap server, silahkan coba beberapa saat lagi")
    #@param kode_promo, kode_transaksi
    #@proccess bergabung dengan room chat promo diadakan. 
    #          Terdapat validasi apakah balance mencukupi dan kode promo valid atau tidak
    #@output -

@bot.message_handler(regexp=r'^/join \w \w$')
def join(message):
    app.logger.debug("'join' command detected")


    #@param kode_transaksi
    #@proccess untuk memasukan token transaksi. Terdapat validasi apakah token valid atau tidak
    #@output pesan berhasil atau tidak

@bot.message_handler(regexp=r'^/token \w$')
def token(message):
    app.logger.debug("'token' command detected")


    #@param kode room chat
    #@proccess untuk mengecheck status dari promo (masih berlaku atau tidak)
    #@output detail dari chat room promo tersebut

@bot.message_handler(regexp=r'^/status \w$')
def status(message):
    app.logger.debug("'status' command detected")


    #@param tanggal start, tanggal berakhir, judul promo, diskon(mungkin dalam persen) jumlah peserta, jumlah balance
    #@proccess untuk membuat promo dan chat room promo tersebut
    #@output detail dari chat room promo tersebut

@bot.message_handler(regexp=r'^/promo$')
def promo(message):
    app.logger.debug("'promo' command detected")


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
