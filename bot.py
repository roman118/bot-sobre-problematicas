import webbrowser, threading
import discord
from discord.ext import commands
import os, random
import requests
import flask
import spacy
from flask import Flask, render_template, request, redirect, url_for

soluciones = {}

# Configura el token de tu bot de Discord
TOKEN = 'token'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Cargar el modelo de spaCy para español
nlp = spacy.load("es_core_news_sm")

@bot.command()
async def analizar(ctx, *, texto: str):
    # Analizar el texto usando spaCy
    doc = nlp(texto)
    
    # Identificar entidades nombradas en el texto
    named_entities = [ent.text for ent in doc.ents if ent.label_ == 'PER']  # Detectar nombres de personas
    
    # Responder con las entidades nombradas detectadas o un mensaje predeterminado si no se detectan entidades
    if named_entities:
        response = f"Entidades nombradas detectadas: {', '.join(named_entities)}"
    else:
        response = "No se detectaron nombres de personas en el texto."

    await ctx.send(response)



@bot.command()
async def open_website(ctx):
    url = "http://127.0.0.1:5500/templates/cambio-climatico.html", "http://127.0.0.1:5500/templates/contaminacao.html", "http://127.0.0.1:5500/templates/calentamiento-global.html"
    webbrowser.open(url)
    await run_flask_and_open_browser()

async def run_flask_and_open_browser():
    loop = asyncio.get_event_loop()
    loop.create_task(run_flask_server())
    await asyncio.sleep(2)  # Asegurémonos de que el servidor esté listo antes de abrir el navegador
    webbrowser.open("http://127.0.0.1:5500/templates/cambio-climatico.html", "http://127.0.0.1:5500/templates/contaminacao.html", "http://127.0.0.1:5500/templates/calentamiento-global.html")

async def run_flask_server():
    app = Flask(__name__)
    app.run(debug=True, threaded=True)

@bot.event
async def on_message(message):
    # Verificar que el mensaje provenga de un usuario y no del bot para evitar bucles
    if message.author == bot.user:
        return

    # Verificar si el contenido del mensaje coincide con lo que estás buscando
    if "calentamiento global" in message.content:
        # Realizar la acción deseada, como enviar un mensaje de respuesta
        await message.channel.send("El calentamiento global es un aumento gradual de la temperatura de la Tierra debido a la liberación de gases de efecto invernadero por actividades humanas como la quema de combustibles fósiles y la deforestación. Estos gases atrapan el calor del sol en la atmósfera, causando impactos como el derretimiento de los casquetes polares y cambios en los patrones climáticos. Para abordarlo, se requiere reducir las emisiones de gases de efecto invernadero y adoptar prácticas más sostenibles. SI QUIERES SABER SOLUCIONES DE ESTO ESCRIBE: solutions")
    if "contaminacion" in message.content:
        # Realizar la acción deseada, como enviar un mensaje de respuesta
        await message.channel.send("La contaminación es la introducción de sustancias o agentes dañinos en el medio ambiente, causando efectos negativos en la salud humana, la vida silvestre y los ecosistemas. Provienen de diversas fuentes como la industria, la agricultura y el transporte. Los principales tipos incluyen contaminación del aire, agua, suelo, acústica y lumínica. Es un problema global que requiere acciones regulatorias, tecnológicas y de concienciación para abordar sus causas y mitigar sus efectos. SI QUIERES SABER SOLUCIONES DE ESTO ESCRIBE: solutions")
    if "cambio climatico" in message.content:
        # Realizar la acción deseada, como enviar un mensaje de respuesta
        await message.channel.send("El cambio climático es un fenómeno que provoca alteraciones a largo plazo en los patrones climáticos de la Tierra. Es principalmente causado por actividades humanas, como la quema de combustibles fósiles y la deforestación, que aumentan las emisiones de gases de efecto invernadero. Estos gases atrapan el calor en la atmósfera, provocando un aumento de la temperatura global. El cambio climático tiene impactos graves en el medio ambiente y la sociedad, como el derretimiento de los glaciares, el aumento del nivel del mar y eventos climáticos extremos. Para combatirlo, se requiere reducir las emisiones y adaptarse a sus efectos. SI QUIERES SABER SOLUCIONES DE ESTO ESCRIBE: solutions")
    if "solutions" in message.content:
        urls = {
            "Cambio Climático": "http://127.0.0.1:5500/templates/cambio-climatico.html",
            "Contaminación": "http://127.0.0.1:5500/templates/contaminacion.html",
            "Calentamiento Global": "http://127.0.0.1:5500/templates/calentamiento-global.html"
        }
        response = "Aquí tienes enlaces a las páginas relacionadas:\n"
        for title, url in urls.items():
            response += f"{title}: {url}\n"
        await message.channel.send(response)

        def check(m):
            return m.author == message.author and m.channel == message.channel

        await message.channel.send("¿Lograste solucionar alguna de estas problemáticas? Si es así, por favor, comparte cómo lo hiciste.")
        try:
            answer = await bot.wait_for('message', check=check, timeout=60)
            soluciones[message.author.id] = answer.content
            await message.channel.send(f"Gracias por compartir cómo solucionaste el problema: {answer.content}")
        except asyncio.TimeoutError:
            await message.channel.send("Se agotó el tiempo para responder.")

@bot.command()
async def ver_soluciones(ctx):
    if soluciones:
        response = "Soluciones dadas hasta el momento:\n"
        for user_id, solucion in soluciones.items():
            member = ctx.guild.get_member(user_id)
            response += f"{member.display_name}: {solucion}\n"
        await ctx.send(response)
    else:
        await ctx.send("No se han dado soluciones hasta el momento.")

# Ejecutar el bot con el token
bot.run(TOKEN)