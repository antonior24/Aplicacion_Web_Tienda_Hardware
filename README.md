# Aplicacion_Web_Tienda_Hardware
Tipos de campo usados (no-relacionales):

CharField

TextField

DecimalField

PositiveIntegerField

IntegerField

BooleanField

DateField

DateTimeField

EmailField

URLField

Parámetros usados (ejemplos, al menos 10 distintos): max_length, unique, blank, null, default, validators, help_text, db_index, choices, max_digits, decimal_places, related_name, on_delete, auto_now_add, unique_together.

Estos parámetros aparecen repartidos por los modelos para cumplir la condición.

```mermaid
erDiagram
    MANUFACTURER ||--o{ PRODUCT : produces
    MANUFACTURER ||--|| COMPANYINFO : has
    CATEGORY ||--o{ PRODUCTCATEGORY : contains
    PRODUCT ||--o{ PRODUCTCATEGORY : categorized_as
    PRODUCT ||--o{ ORDERITEM : included_in
    ORDER ||--o{ ORDERITEM : contains
    ORDER ||--|| SHIPMENTDETAIL : has
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER ||--|| PROFILE : has
    CUSTOMER }o--o{ PRODUCT : wishlist

    MANUFACTURER {
        string name
        string website
        date established
        bool active
    }

    COMPANYINFO {
        string vat_number
        string contact_email
        text address
    }

    CATEGORY {
        string name
        string slug
        text description
    }

    PRODUCT {
        string sku
        string name
        text description
        decimal price
        int stock
    }

    PRODUCTCATEGORY {
        bool featured
        int display_order
    }

    CUSTOMER {
        string first_name
        string last_name
        string email
        string phone
    }

    PROFILE {
        date birth_date
        bool newsletter
        text notes
    }

    ORDER {
        datetime created_at
        char status
        decimal total
    }

    SHIPMENTDETAIL {
        string tracking_code
        date shipped_date
        date delivery_estimate
    }


Modelos y explicación (extracto breve)

Manufacturer: fabricante; name (CharField, max_length=100, unique=True), website (URLField), established (DateField), active (BooleanField).

CompanyInfo: información fiscal y contacto del fabricante; manufacturer (OneToOneField), vat_number (CharField), contact_email (EmailField), address (TextField).

Category: categorías jerárquicas; parent es ForeignKey a self (on_delete=models.SET_NULL) para permitir categorías top-level.

Product: producto comercial; sku (único), price (DecimalField con max_digits y decimal_places y validator MinValueValidator(0)), stock (PositiveIntegerField), manufacturer (ForeignKey).

ProductCategory: tabla intermedia para atributos extras en la relación Product-Category; featured y display_order.

Customer: cliente; email único; wishlist ManyToMany a Product.

Profile: datos extendidos del cliente (OneToOne).

Order: pedido; status con choices (P, C, X), total DecimalField, products ManyToMany a Product through OrderItem.

ShipmentDetail: detalles de envío (OneToOne con Order)

OrderItem: línea del pedido (tabla intermedia entre Order y Product) con quantity y unit_price.

Parámetros usados (explicación corta)

max_length: longitud máxima para CharField y SlugField.

unique: obliga unicidad en base de datos.

null/blank: control de valores nulos y formularios.

default: valor por defecto.

validators: validadores (p.ej. MinValueValidator).

choices: lista de tuplas para limitar valores.

help_text, db_index, related_name, on_delete, auto_now_add — explicado brevemente en el README.

Explicación de código no visto en clase (más detallada)

unique_together (Meta): obliga unicidad combinada entre campos (product, category) para evitar duplicados en la tabla intermedia.

related_name: nombre inverso para relaciones (ej. manufacturer.products) que facilita consultas desde la instancia objetivo.

on_delete opciones: CASCADE, PROTECT, SET_NULL — se usan según la semántica: PROTECT evita borrar fabricantes si hay productos; SET_NULL permite mantener categorías si el padre se borra.

validators: se usan con campos numéricos para asegurar rangos.

auto_now_add=True en created_at guarda la fecha de creación automáticamente.
