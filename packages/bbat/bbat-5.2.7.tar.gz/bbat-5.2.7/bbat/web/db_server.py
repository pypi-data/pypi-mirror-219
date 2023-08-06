from bbat.web.sanic_app import app, success, error
from bbat.web.url_to_sql.query import Query


# get方法查询函数
@app.route("/hyper/<table>", methods=["GET"])
async def query(request, table):
    db = request.app.ctx.db
    result = {}
    query_string = request.query_string
    query = Query(table, query_string)

    sql = query.to_sql()
    # 1.主表查询
    data = await db.query(sql)
    # 根据field定义，做数据处理
    data = query.data_convert(query.fields, data)
    # 2.统计查询
    info = await db.fetch(query.to_count_sql())
    result['meta'] = {"total": info['cnt']}
    # 3.子表查询
    for relation in query.relation:
        # master表外键所有id
        idhub = set([str(i[relation.master_key]) for i in data])
        if len(idhub) == 0:
            continue
        ids = ",".join([ f"'{i}'" for i in idhub])
        # 查子表数据
        sql = relation.to_sql(f"{relation.relate_key} IN ({ids})")
        print("SUBQUERY SQL>>>", sql)
        relation_data = await db.query(sql)
        query.data_convert(relation.fields, relation_data)
        # 合并数据
        relation.merge_table_data(data, relation_data)

    result['list'] = data
    return success(result)

# POST,PUT方法，插入和更新数据，有查询条件触发更新
@app.route("/hyper/<table>", methods=["POST", "PUT"])
async def post(request, table):
    db = request.app.ctx.db
    query_string = request.query_string
    data = request.json
    if not data:
        return error("ERROR: data is null")
    # 有query触发更新
    query = Query(table, query_string)
    if query_string:
        sql = query.to_update_sql(data)
        result = await db.execute(sql)
        return success(result)
    else:
        sql = query.to_insert_sql(data)
        result = await db.execute(sql)
        return success(result)

# delete data
@app.route("/hyper/<table>", methods=["DELETE"])
async def delete(request, table):
    db = request.app.ctx.db
    query_string = request.query_string
    # 有query触发更新
    query = Query(table, query_string)
    if query_string:
        result = await db.execute(query.to_delete_sql())
        return success(result)
    else:
        return error("ERROR: No query string")
    
# 创建表
@app.route("/hyper/table", methods=["POST"])
async def create_table(request):
    db = request.app.ctx.db
    table = request.args.get('name')
    res = await db.create_table(table)
    return success(res.lastrowid)

# 查所有表
@app.route("/hyper/table", methods=["GET"])
async def get_tables(request):
    db = request.app.ctx.db
    database = db.db_args['db']
    tables = await db.tables(database=database)
    return success(tables)

# 查表结构
@app.route("/hyper/table_field", methods=["GET"])
async def table_struct(request):
    db = request.app.ctx.db
    # 指定表
    table = request.args.get('name')
    if not table:
        raise ValueError("No table")
    table_info = await db.table_fields(name=table)
    return success(table_info)

# 添加字段
@app.route("/hyper/table_field", methods=["POST"])
async def add_field(request):
    db = request.app.ctx.db
    json = request.json
    table = json.get('table')
    field = json.get('field')
    type = json.get('type')
    if not all([table, field, type]):
        return ValueError('Invalid data')
    res = await db.add_field(table=table, field=field, type=type)
    return success(res)

# 删除字段
@app.route("/hyper/table_field", methods=["DELETE"])
async def del_field(request):
    db = request.app.ctx.db
    json = request.json
    table = json.get('table')
    field = json.get('field')
    if not all([table, field, type]):
        return ValueError('Invalid data')
    res = await db.drop_field(table=table, field=field)
    return success(res)
