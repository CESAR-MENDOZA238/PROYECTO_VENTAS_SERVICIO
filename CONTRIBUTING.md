# Guía para colaboradores — Proyecto Ventas Servicio

Bienvenido/a al proyecto. Esta guía te lleva paso a paso desde clonar el repo hasta subir tu primer cambio.

## 1. Clona el repositorio

git clone https://github.com/CESAR-MENDOZA238/PROYECTO_VENTAS_SERVICIO.git
cd PROYECTO_VENTAS_SERVICIO

## 2. Cambia a tu rama de trabajo

No trabajes directo sobre main. Ya existen ramas creadas para cada área:

Si trabajas en backend:
git checkout feature/backend-setup

Si trabajas en frontend:
git checkout feature/frontend-setup

## 3. Configura tu entorno local

### Backend (Python)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Copia .env.example como .env en la raíz del proyecto y completa los valores (pídeselos a César, nunca se suben a GitHub).

### Frontend
cd frontend
npm install

Copia .env.example como .env dentro de frontend/.

## 4. Reglas importantes

- Nunca subas archivos .env, ya están en .gitignore, pero verifica con git status antes de hacer git add .
- Trabaja solo dentro de tu área (backend o frontend) para evitar conflictos con el otro colaborador.
- Haz commits pequeños y frecuentes, no un solo commit gigante al final.

## 5. Flujo de trabajo diario

Antes de empezar a trabajar cada día, trae los cambios más recientes:
git checkout main
git pull origin main
git checkout feature/tu-rama
git merge main

Mientras trabajas, guarda tu progreso:
git add .
git commit -m "descripcion corta de lo que hiciste"
git push origin feature/tu-rama

## 6. Cuando termines una funcionalidad

1. Ve a GitHub, tu repositorio.
2. Verás un botón "Compare & pull request" en tu rama.
3. Escribe un título y descripción breve de lo que hiciste.
4. Abre el Pull Request hacia main.
5. Espera a que César lo revise y apruebe antes de que se fusione.

## 7. Si hay un conflicto de merge

Edita el archivo a mano, decide qué código se queda, borra las marcas <<<<<<<, =======, >>>>>>>, y luego:
git add archivo-resuelto
git commit
git push origin feature/tu-rama

## 8. Convención de nombres de ramas

- feature/backend-... nuevas funcionalidades del backend
- feature/frontend-... nuevas funcionalidades del frontend
- fix/... corrección de bugs
- hotfix/... arreglos urgentes

Ejemplo: feature/backend-login, feature/frontend-catalogo-ventas

Cualquier duda, contacta a César Mendoza (dueño del repositorio).