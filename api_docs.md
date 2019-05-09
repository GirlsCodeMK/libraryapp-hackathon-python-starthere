# GirlsCode MK Library API reference

## Formats

The API supports most HTTP verbs most of the time, but generally use only `GET` and `POST` to interact with the data.

The API only returns JSON format responses.

Dates are in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format, such as `YYYY-MM-DD`; for example, `2019-07-29`.

All responses are paginated, with ten responses per page. Responses include `previous` and `next` links for different pages as necessary.

Responses use HATEOAS links to hyperlink to additional information. 

### Example response

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "url": "http://localhost:8000/library/api/v1/books/2/",
            "title": "Advanced Django",
            "author": "Django author",
            "isbn": "43253",
            "copy_available": true,
            "copies": [
                "http://localhost:8000/library/api/v1/copies/3/",
                "http://localhost:8000/library/api/v1/copies/16/"
            ]
        },
        {
            "url": "http://localhost:8000/library/api/v1/books/1/",
            "title": "Beginning Django",
            "author": "Django author",
            "isbn": "12234",
            "copy_available": true,
            "copies": [
                "http://localhost:8000/library/api/v1/copies/1/",
                "http://localhost:8000/library/api/v1/copies/2/",
                "http://localhost:8000/library/api/v1/copies/17/"
            ]
        }
    ]
}
```

## Authentication

Authentication is by user token. Use the app admin panel to generate and examine tokens for users.

The authentication token is passed in a header with the format: 

```
Authorization:Token 856ac7748c34565498168ae500f2ccd7629a2fd2
```

Note the single space between the `Token` literal in the start of the token itself.

## Books

Book information is readable by unauthenticated users. Only users in the `Librarian` group can write to the books collection.

Book information includes links to all copies of that book.

These `GET` requests will return information about one or more books. 

* `/library/api/v1/books/`: return information on all books.
* `/library/api/v1/books`: return information on all books.
* `/library/api/v1/books/1`: return information on a specific book with ID = `1`.
* `/library/api/v1/books?search=django`: return all books with `django` in author or title fields. Search is case-insensitive and partial matches are allowed.
* `/library/api/v1/books?search=django,begin`: return all books with `django` in author or title fields _and_ `begin` in author or title fields. Search is case-insensitive and partial matches are allowed.
* `/library/api/v1/books?search=django%20begin`: return all books with `django` in author or title fields _and_ `begin` in author or title fields. Search is case-insensitive and partial matches are allowed.
* `/library/api/v1/books?title=Advanced%20Django`: return all books with the title `Advanced Django`. Searching is exact and case sensitive. 
* `/library/api/v1/books?author=Django%20author`: return all books with the author `Django author`. Searching is exact and case sensitive. 

### Updating

`POST` to `/library/api/v1/books/` to create a new book or update an existing book. 

`PUT` to `/library/api/v1/books/99` to replace all the fields of an existing book with id = 99. 

`PATCH` to `/library/api/v1/books/99` to update just some fields of an existing book. 

## Copies

Book copy information is readable by unauthenticated users. Only users in the `Librarian` group can write to the copy collection.

These `GET` requests will return information about one or more books. 

* `/library/api/v1/copies/`: return information on all book copies.
* `/library/api/v1/copies`: return information on all book copies.
* `/library/api/v1/copies/1`: return information on a specific book copy with ID = `1`. (Note this may not be the "copy number" of the book copy)

### Updating

`POST` to `/library/api/v1/copies/` to create a new copy or update an existing copy. 

`PUT` to `/library/api/v1/copies/99` to replace all the fields of an existing copy with id = 99. 

`PATCH` to `/library/api/v1/copies/99` to update just some fields of an existing copy. 

Use these one-letter codes to describe the condition of a copy:

| Code | Condition |
|:----:|:---------:|
| `M`  | Mint      |
| `G`  | Good      |
| `W`  | Worn      |
| `D`  | Damaged   |
| `L`  | Lost      |
| `X`  | Destroyed |

## Loans

Loan information is not visible to unauthenticated users. 

Authenticated users can view their own loans at the `myloans` endpoint. This defaults to only responding with open loans (unreturned book copies). Use the `closed=True` parameter to return instead closed loans (where the book has been returned).

These `GET` requests will return information about one or more loans. 

* `/library/api/v1/myloans/`: return information on all of the current user's open loans.
* `/library/api/v1/myloans`: return information on all of the current user's open loans.
* `/library/api/v1/myloans?closed=True`: return information on all of the current user's closed loans.
* `/library/api/v1/myloans/19409af1-48e9-464a-a629-e220059a81ac/`: return information on a specific **open** loan with ID = `19409af1-48e9-464a-a629-e220059a81ac`, so long as it is one of the current user's loans.
* `/library/api/v1/myloans/19409af1-48e9-464a-a629-e220059a81ac/?closed=True`: return information on a specific **closed** loan with ID = `19409af1-48e9-464a-a629-e220059a81ac`, so long as it is one of the current user's loans. 

Authenticated users in the `Librarian` group can view loans for any user, and can write to the Loan collection.

* `/library/api/v1/loans/`: return information on all of the open loans.
* `/library/api/v1/loans`: return information on all of the open loans.
* `/library/api/v1/loans?closed=True`: return information on all of the closed loans.
* `/library/api/v1/loans/19409af1-48e9-464a-a629-e220059a81ac/`: return information on a specific **open** loan with ID = `19409af1-48e9-464a-a629-e220059a81ac`.
* `/library/api/v1/loans/19409af1-48e9-464a-a629-e220059a81ac/?closed=True`: return information on a specific **closed** loan with ID = `19409af1-48e9-464a-a629-e220059a81ac`. 


### Updating

`POST` to `/library/api/v1/loans/` to create a new loan or update an existing loan. 

`PUT` to `/library/api/v1/loans/99` to replace all the fields of an existing loan with id = 99. 

`PATCH` to `/library/api/v1/loans/99` to update just some fields of an existing loan. 

## Users

User information is not available across this API.
