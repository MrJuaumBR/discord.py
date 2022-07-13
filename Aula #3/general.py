import sqlite3 as sql

class general():
  def table(database,nome,valores):
    cursor = database.cursor()
    cursor.execute(
      f"""
      CREATE TABLE IF NOT EXISTS {nome}({valores})
      """
    )
    database.commit()

  def get(database,table,coluna,valor):
    cursor = database.cursor()
    val = cursor.execute(
      f"""
      SELECT {coluna} FROM {table} WHERE id = {valor}
      """
    ).fetchone()
    return val
    # (, "seu valor") "seu valor"
  def insert(database,table,valor): # objeto, nome, tupla
    cursor = database.cursor()
    cursor.execute(
      f"""
      INSERT INTO {table} ({valor[0]}) VALUES({valor[1]})
      """
    )
    database.commit() # Salva as alterações
  def update(database,table,parametros,condicoes):
    # Update atualiza um dado ja existente Ex: na tabela
    # 5 Atum => 7 Atum, ? Error, Valor não foi inserido
    cursor = database.cursor()
    cursor.execute(
      f"""
      UPDATE {table} SET {parametros[0]} = {parametros[1]} WHERE id = {condicoes}
      """
    )
    database.commit()

