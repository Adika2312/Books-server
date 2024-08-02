from flask import Flask, request, jsonify

app = Flask(__name__)
app.json.sort_keys = False
books = []
book_id = 1


# HEALTH
@app.route('/books/health', methods=['GET'])
def health():
    return 'OK', 200


# CREATE NEW BOOK
@app.route('/book', methods=['POST'])
def create_new_book():
    global book_id
    global books
    json_data = request.get_json()
    book_title = json_data.get('title')

    for book in books:
        if book['title'].lower() == book_title.lower():
            return jsonify(errorMessage=f"Error: Book with the title [{json_data['title']}] already exists in the system"), 409

    book_year = json_data['year']
    if book_year < 1940 or book_year > 2100:
        return jsonify(errorMessage=f"Error: Can't create new Book that its year [{book_year}] is not in the accepted range [1940 -> 2100]"), 409

    book_price = json_data['price']
    if book_price < 0:
        return jsonify(errorMessage=f"Error: Can't create new Book with negative price"), 409

    new_book = {
        'id': book_id,
        'title': book_title,
        'author': json_data['author'],
        'year': book_year,
        'price': book_price,
        'genres': json_data['genres']
    }
    book_id += 1
    books.append(new_book)
    return jsonify(result=new_book['id']), 200


# GET TOTAL BOOKS
@app.route('/books/total', methods=['GET'])
def get_total_books():
    requested_books = filter_books(request.args)
    return jsonify(result=len(requested_books)), 200


# GET BOOKS DATA
@app.route('/books', methods=['GET'])
def get_books_data():
    requested_books = filter_books(request.args)
    return jsonify(result=sorted(requested_books, key=lambda x: x['title'].lower())), 200


# GET SINGLE BOOK DATA
@app.route('/book', methods=['GET'])
def get_single_book_data():
    requested_book_id = int(request.args.get('id'))
    for book in books:
        if book['id'] == requested_book_id:
            return jsonify(result=book), 200

    return jsonify(errorMessage=f"Error: no such Book with id {requested_book_id}"), 404

# UPDATE BOOK PRICE
@app.route('/book', methods=['PUT'])
def update_book_price():
    requested_book_id = int(request.args.get('id'))
    new_price = int(request.args.get('price'))

    if new_price <= 0:
        return jsonify(errorMessage=f"Error: price update for book [{requested_book_id}] must be a positive integer"), 409

    for book in books:
        if book['id'] == requested_book_id:
            old_price = book['price']
            book['price'] = new_price
            return jsonify(result=old_price), 200

    return jsonify(errorMessage=f"Error: no such Book with id {requested_book_id}"), 404

# DELETE BOOK
@app.route('/book', methods=['DELETE'])
def delete_book():
    requested_book_id = int(request.args.get('id'))
    for book in books:
        if book['id'] == requested_book_id:
            books.remove(book)
            return jsonify(result=len(books)), 200

    return jsonify(errorMessage=f"Error: no such Book with id {requested_book_id}"), 404


def filter_books(args):
    filtered_books = list(books)

    for book in filtered_books:
        is_book_to_remove = False
        if 'author' in args:
            if book['author'].lower() != args['author'].lower():
                is_book_to_remove = True
        if 'price-bigger-than' in args:
            if book['price'] < int(args['price-bigger-than']):
                is_book_to_remove = True
        if 'price-less-than' in args:
            if book['price'] > int(args['price-less-than']):
                is_book_to_remove = True
        if 'year-bigger-than' in args:
            if book['year'] < int(args['year-bigger-than']):
                is_book_to_remove = True
        if 'year-less-than' in args:
            if book['year'] > int(args['year-less-than']):
                is_book_to_remove = True
        if 'genres' in args:
            genres = set(args['genres'].split(','))
            if set(book['genres']).isdisjoint(genres):
                is_book_to_remove = True
        if is_book_to_remove == True:
            filtered_books.remove(book)

    return filtered_books


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8574)