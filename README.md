Link al proyecto: https://webstore-xb8n.onrender.com/
# 🛒 Online Store

Una tienda en línea construida con Django que permite compras tanto para usuarios registrados como invitados. Los usuarios pueden navegar productos, agregar artículos al carrito, realizar pagos con Stripe, y guardar direcciones de envío. El backend se conecta con Supabase como base de datos, Render como plataforma de despliegue, y Cloudinary para el almacenamiento de imágenes.

---

## 🚀 Tecnologías Utilizadas

### 🔧 Backend
- **Django**: Framework web robusto y escalable en Python.
- **Supabase**: Base de datos PostgreSQL autoadministrada, usada como backend remoto para persistencia de datos.
- **Stripe**: API de pagos para manejar checkout, pagos con tarjeta y clientes invitados.
- **Cloudinary**: Servicio para alojar imágenes y cargarlas dinámicamente en los productos.
- **Render**: Plataforma de despliegue usada para publicar la aplicación en producción.

### 🎨 Frontend
- **HTML5 + CSS3**: Para las vistas del sitio.
- **Bootstrap 5**: Framework CSS para estilos responsivos y rápidos.
- **JavaScript**: Para interactividad en tiempo real como actualización de cantidades en el carrito.

---

## ⚙️ Funcionalidades Clave

- ✔️ Registro y login de usuarios
- ✔️ Compra como usuario invitado (sin sesión iniciada)
- ✔️ Checkout dinámico con validación de dirección de envío
- ✔️ Integración con Stripe para pagos
- ✔️ Visualización de órdenes y estado de compra
- ✔️ Gestión de imágenes de productos con Cloudinary
- ✔️ Panel de administración de Django para CRUD de productos
- ✔️ Persistencia de carrito para usuarios logueados y anónimos

---

## 📂 Estructura del Proyecto

online_store/
│
├── carrito/ # App del carrito y proceso de pago
├── main/ # App principal (productos, homepage, etc.)
├── users/ # Gestión de usuarios y perfiles
├── templates/ # Archivos HTML
├── static/ # Archivos CSS, JS, imágenes locales
├── media/ # Archivos subidos (si no se usa Cloudinary)
├── manage.py
└── requirements.txt


---

## 🛠️ Configuración

### Variables de entorno requeridas:

```env
# Stripe
STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx

# Cloudinary
CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>

# Supabase
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<db_name>
