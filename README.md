<div align="center">

<img src="assets/logo.png" alt="Khipu - Asistente de Almacén IA" width="520">

### Consulta, planifica y reserva componentes y laboratorios de la FIEE-UNMSM

![Hackathon](https://img.shields.io/badge/ENEISOFT_2026-XVI_edición-0B1F3A?style=for-the-badge)
![Eje](https://img.shields.io/badge/Gestión_universitaria-IA_aplicada-1E6BFF?style=for-the-badge)
![Estado](https://img.shields.io/badge/estado-MVP_funcionando-1B8A4B?style=for-the-badge)

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?logo=googlegemini&logoColor=white)

<br>

[![Abrir Khipu](https://img.shields.io/badge/▶_ABRIR_KHIPU-khipu--fiee.streamlit.app-FFB000?style=for-the-badge&labelColor=0B1F3A)](https://khipu-fiee.streamlit.app)

Funciona desde el celular o la laptop, sin instalar nada: **[khipu-fiee.streamlit.app](https://khipu-fiee.streamlit.app)**

</div>

---

## Contenido

- [Pruébalo en un minuto](#pruébalo-en-un-minuto)
- [¿Por qué "Khipu"?](#por-qué-khipu)
- [El contexto](#el-contexto)
- [El problema](#el-problema)
- [Lo que proponemos](#lo-que-proponemos)
- [Qué puedes hacer en Khipu](#qué-puedes-hacer-en-khipu)
- [Capturas](#capturas)
- [Cómo usamos la IA](#cómo-usamos-la-ia)
- [Seguridad](#seguridad)
- [Cómo está construido](#cómo-está-construido)
- [Lo que viene](#lo-que-viene)
- [Correrlo en tu computadora](#correrlo-en-tu-computadora)
- [Lo que aprendimos](#lo-que-aprendimos)
- [Quiénes somos](#quiénes-somos)

---

## Pruébalo en un minuto

1. Entra a **[khipu-fiee.streamlit.app](https://khipu-fiee.streamlit.app)**. Si nadie la ha usado en un rato, tarda unos segundos en despertar.
2. En **Preguntar a Khipu**, escribe algo como *"¿hay 2N2222? necesito 2, agrégalo"*, o sube la foto de un componente o el PDF de tu guía.
3. En **Armar un proyecto**, cuéntale tu idea (*"un robot seguidor de línea con Arduino"*) y pasa la lista a **Mi lista**.
4. En **Reservar Laboratorio**, toca una franja libre del calendario semanal, pon los datos de tu grupo y confirma la reserva con el código que te llega al correo de San Marcos.
5. En **Compra y Venta**, mira lo que otros estudiantes venden o publica lo que ya no usas.
6. Si quieres ver el otro lado, cambia a **Encargado** en el selector de modo. La clave te la damos nosotros.

---

## ¿Por qué "Khipu"?

Los incas llevaban el registro de sus almacenes (*qollqas*), censos e inventarios con el **khipu**: un cordón principal del que colgaban cuerdas con nudos, y cada nudo guardaba un dato.

Nos pareció la metáfora perfecta. Nuestro logo es un cordón del que cuelgan componentes electrónicos, y las pestañas de la app tienen la misma forma. Khipu es, en el fondo, el registro del almacén de nuestra facultad, hecho por estudiantes de Electrónica para estudiantes.

<img width="714" height="430" alt="image" src="https://github.com/user-attachments/assets/df1e6171-792a-4135-a57d-9ba25af89bc0" />

---

## El contexto

En la **Facultad de Ingeniería Electrónica y Eléctrica (FIEE)** de San Marcos armamos circuitos desde los primeros ciclos: fuentes, amplificadores, sistemas digitales, robots, proyectos IoT.

<img width="903" height="512" alt="image" src="https://github.com/user-attachments/assets/5e0a9cba-22b2-40d8-9cfd-06063860279c" />

Para eso la facultad tiene dos recursos clave:

- **Un almacén** con circuitos integrados, transistores, conectores, resistencias, capacitores, sensores, módulos y más, que se prestan a los estudiantes.
- **Laboratorios de electrónica** que se piden formalmente y se rigen por el *Reglamento General de los Laboratorios de Electrónica* (R.D. N.° 000989-2023-D-FIEE/UNMSM).

El detalle es que los componentes solo se pueden usar dentro de un laboratorio, y hoy todo depende de ir en persona, preguntar y llenar formatos a mano.

---

## El problema

Esto lo vivimos cada ciclo:

- Vas al almacén **sin saber si hay** lo que necesitas, y muchas veces te regresas con las manos vacías.
- **No sabes qué componentes pide tu proyecto** hasta leerte toda la guía, a veces minutos antes de entrar a clase.
- Si algo falta, **nadie te dice qué lo puede reemplazar**, así que terminas comprando en Paruro algo que la facultad sí tenía.
- Hay componentes con **marcas tan pequeñas o borrosas** que cuesta saber qué son.
- Reservar un laboratorio es un **trámite manual**: formato, datos de al menos dos estudiantes, firmas y correo a la jefatura.
- Y el almacén **no sabe qué buscan los alumnos**, así que no puede anticipar qué comprar.

<img width="772" height="507" alt="image" src="https://github.com/user-attachments/assets/7b1e18ca-0b3a-4cf8-aea8-761699c42cf8" />
<img width="900" height="496" alt="image" src="https://github.com/user-attachments/assets/9bc08be3-22dd-48f8-b47e-3ea51df53fa2" />
<img width="758" height="502" alt="image" src="https://github.com/user-attachments/assets/7d527880-1f52-4412-801e-42d7ae5b6810" />

---

## Lo que proponemos

Una sola app web que te acompaña desde que tienes la idea del proyecto hasta que tienes el laboratorio y los componentes reservados.

```mermaid
flowchart LR
    A["Pregunto, subo una foto<br/>o el PDF de mi guía"] --> C
    B["Cuento mi proyecto"] --> C
    C{"¿Hay en<br/>la FIEE?"} -- Sí --> D["Mi lista"]
    C -- No --> E["Equivalente<br/>disponible"] --> D
    D --> F["Reservo laboratorio<br/>(2 h) + componentes"]
    F --> H["Confirmo con el código<br/>de mi correo UNMSM"]
    H --> G["El encargado<br/>acepta o rechaza"]
    G --> I["Me llega el aviso<br/>por correo"]
```

Lo que el chat o tu proyecto te recomiendan se va guardando en **Mi lista**, y cuando reservas el laboratorio esos componentes ya están cargados. No tienes que volver a preguntar ni anotar nada.

<img width="1600" height="560" alt="image" src="https://github.com/user-attachments/assets/c71b1601-efab-418b-a686-0f7cb35b4e60" />

---

## Qué puedes hacer en Khipu

Arriba a la derecha eliges si entras como **estudiante** o como **encargado**.

### Preguntar a Khipu

Es un chat al que le hablas como a un compañero, y también le puedes mandar archivos:

| Si le mandas… | Khipu… |
|---|---|
| *"¿Hay LM358?"*, *"necesito 2 transistores 2N2222"* | Te dice cuántos hay y en qué estante. Si no hay, te propone equivalentes que sí están, con sus advertencias (*"ojo, el pinout es distinto"*). |
| La **foto** de un componente | Lo reconoce por el encapsulado y las marcas, te dice qué tan seguro está y si hay en el almacén. |
| El **PDF** de tu guía o informe | Te resume la experiencia, te dice qué componentes necesitas, revisa si están en la facultad y te da un par de consejos. |
| *"¿Hay laboratorio libre el lunes de 2 a 4?"* | Revisa los horarios y te dice qué laboratorios están libres y por qué los demás no. |

Si le dices *"agrégalo"*, lo pone en tu lista. Y algo importante: **Khipu no inventa stock**. Si algo no está en el inventario, te lo dice.

### Armar un proyecto

Le cuentas qué quieres armar y te devuelve la lista de componentes, para qué sirve cada uno, si hay, si falta o si no existe en el almacén, qué equivalentes puedes usar y algunos consejos. Con un clic pasa todo a tu lista. La tomamos como un punto de partida: siempre conviene revisar el datasheet.

### Reservar Laboratorio

1. Abres el **calendario semanal** (lunes a sábado, franjas de 2 horas de 08:00 a 20:00) y tocas una casilla libre: la fecha, el horario y el laboratorio se llenan solos. Lo ocupado por clases u otras reservas aparece en gris.
2. Pones el motivo y los datos del grupo (mínimo dos personas). El de la primera fila es el **líder** y pone su correo `@unmsm.edu.pe`.
3. Los componentes de tu lista ya aparecen, con lo que realmente hay disponible en esa franja.
4. Te llega un **código de 6 dígitos** al correo del líder; lo escribes y recién ahí se guarda la reserva.
5. Recibes tu código `LAB-XXXX`, un comprobante para descargar y un correo con todo el detalle.

¿Cerraste la página? En *Consultar mi solicitud* pones tu **código de alumno** y ves todas tus reservas y en qué estado están. Cuando el encargado responde, también te llega un correo.

### Compra y Venta

Un espacio para comprar y vender componentes entre estudiantes de la facultad. Quien publica confirma con un código en su correo `@unmsm.edu.pe`, el encargado revisa el aviso antes de que aparezca, y cada publicación muestra el contacto del vendedor (correo y, si quiere, WhatsApp). Khipu no cobra ni intermedia: el trato es entre estudiantes.

### Encargado

Con su clave, el encargado ve cuántas solicitudes tiene pendientes (se actualiza sola cada pocos segundos y avisa cuando llega una nueva). Desde ahí puede:

- revisar cada solicitud y aceptarla o rechazarla con una nota;
- actualizar el inventario y el stock;
- editar los laboratorios y el horario de clases;
- ver qué es lo más pedido y qué está agotado, para planificar compras.

---

## Capturas

<table>
  <tr>
    <td width="50%"><img src="assets/capturas/inicio.png" alt="Inicio de Khipu"><br><sub><b>Inicio.</b> Presentación, cifras del almacén y acceso a las cuatro herramientas.</sub></td>
    <td width="50%"><img src="assets/capturas/chat-pdf.png" alt="Chat analizando un PDF"><br><sub><b>Preguntar a Khipu con un PDF.</b> Resume la guía, lista los componentes con su stock real y da consejos.</sub></td>
  </tr>
  <tr>
    <td><img src="assets/capturas/chat-foto.png" alt="Chat identificando un componente por foto"><br><sub><b>Preguntar a Khipu con una foto.</b> Identifica el integrado por sus marcas, indica su nivel de confianza y lo busca en el almacén.</sub></td>
    <td><img src="assets/capturas/proyecto.png" alt="Armar un proyecto"><br><sub><b>Armar un proyecto.</b> De una idea a la lista de materiales, cruzada con el stock y la ubicación.</sub></td>
  </tr>
  <tr>
    <td><img src="assets/capturas/calendario.png" alt="Calendario semanal de laboratorios"><br><sub><b>Reservar Laboratorio.</b> Calendario semanal con las franjas libres; la casilla elegida queda resaltada.</sub></td>
    <td><img src="assets/capturas/compra-venta.png" alt="Compra y Venta"><br><sub><b>Compra y Venta.</b> Publicaciones entre estudiantes, revisadas por el encargado.</sub></td>
  </tr>
</table>

---

## Cómo usamos la IA

No entrenamos un modelo propio. Lo que hicimos fue conectar modelos que ya existen a datos reales de la facultad, de forma que la IA nunca tenga que adivinar.

- **El chat es un agente con herramientas.** El modelo no tiene el inventario en la memoria: para responder tiene que consultar nuestra base de datos con cuatro funciones (`buscar_en_almacen`, `ver_equivalentes`, `ver_laboratorios_libres` y `agregar_a_mi_lista`).
- **Fotos y PDFs en la misma conversación.** Usamos un modelo multimodal que lee imágenes y documentos, y después verifica todo contra el inventario.
- **Mi proyecto** pide al modelo una respuesta en formato JSON, y el cruce con el stock y los equivalentes lo hace Python, sin IA, para que sea exacto.
- **Si un modelo se satura**, Khipu pasa automáticamente al siguiente sin perder la conversación.

```mermaid
sequenceDiagram
    participant E as Estudiante
    participant K as Khipu (LLM)
    participant DB as Inventario FIEE
    E->>K: ¿Hay 2N2222? Necesito 2
    K->>DB: buscar_en_almacen("2N2222")
    DB-->>K: stock = 0
    K->>DB: ver_equivalentes("2N2222A")
    DB-->>K: PN2222A (30), 2N3904 (25)
    K-->>E: No hay 2N2222A. Puedes usar PN2222A (revisa el pinout)
```

Lo que más nos enorgullece: las equivalencias entre componentes no las inventa la IA. Las armamos y revisamos nosotros con los datasheets, porque eso es justamente lo que aprendemos en la carrera.

---

## Seguridad

Un mentor nos hizo una pregunta clave: *¿qué impide que alguien reserve a nombre de otro?* Esto fue lo que hicimos:

- **Confirmación con el correo institucional.** Antes de guardar la reserva, Khipu manda un código de 6 dígitos al correo `@unmsm.edu.pe` del líder. Solo quien tiene acceso a ese correo puede confirmar. El código vence en 10 minutos y hay un máximo de intentos.
- **Sello digital.** Cada reserva se guarda con una huella SHA-256 de sus datos. Si alguien la modifica después, el encargado lo ve de inmediato.
- **Validaciones sin IA.** Que el laboratorio esté libre, que alcance el stock en esa franja y que haya al menos dos estudiantes lo revisa Python, no el modelo.
- **El panel del encargado** pide una clave que vive en el servidor, no en el código.

Más adelante, la idea es pasar a un inicio de sesión con la cuenta de San Marcos y a firma digital con DNIe.

---

## Cómo está construido

```mermaid
flowchart TB
    subgraph UI["Interfaz · Streamlit (celular y PC)"]
        P[Preguntar]
        PR[Mi proyecto]
        L[Laboratorio]
        EN[Encargado]
        ML[(Mi lista)]
    end
    subgraph IA["Inteligencia artificial"]
        CH[ia_chat · herramientas + fotos + PDFs]
        IP[ia_proyecto · idea → JSON]
    end
    subgraph DATOS["Datos · SQLite"]
        DB[(componentes · equivalencias<br/>laboratorios · horarios<br/>solicitudes firmadas)]
    end
    P --> CH
    PR --> IP
    CH & IP --> GEM[Google Gemini API]
    CH & PR --> ML --> L
    CH & IP & L & EN --> DB
    L & EN --> MAIL[Correos: código, confirmación y avisos]
```

- **Python y Streamlit** para la app web.
- **Streamlit Community Cloud** para publicarla: todos usan el mismo servidor, así que lo que reserva un alumno el encargado lo ve al instante.
- **SQLite** para el inventario, los laboratorios y las reservas.
- **Google Gemini** para el chat, las fotos, los PDFs y las listas de proyectos.
- **Gmail (SMTP) y SHA-256** para los correos y el sello de cada reserva.

Por ahora trabajamos con un inventario de ejemplo de 95 componentes e instrumentos que usamos en los cursos, y con laboratorios y horarios también de ejemplo. Cargar los datos reales es cuestión de reemplazar los archivos de `data/` o editarlos desde el panel del encargado.

---

## Lo que viene

Lo que ya funciona:

- [x] Chat con inventario real, equivalentes, fotos, PDFs y laboratorios libres
- [x] Lista de componentes a partir de la idea del proyecto
- [x] Mi lista compartida entre pestañas
- [x] Reserva de laboratorio con calendario semanal, componentes y stock por franja
- [x] Compra y Venta entre estudiantes, con publicaciones revisadas por el encargado
- [x] Página de inicio, misión y visión, preguntas frecuentes y modo oscuro
- [x] Confirmación con código al correo institucional y sello digital
- [x] Comprobante, correo de confirmación y aviso cuando el encargado responde
- [x] Panel del encargado en tiempo real
- [x] Publicada en [khipu-fiee.streamlit.app](https://khipu-fiee.streamlit.app)

Lo que nos gustaría hacer después:

- [ ] Iniciar sesión con la cuenta `@unmsm.edu.pe`
- [ ] Firma digital con DNIe (RENIEC)
- [ ] Una base de datos en la nube, para que nada se pierda si el servidor se reinicia
- [ ] Un foro para compartir proyectos y dudas
- [ ] Trabajar con el inventario real del almacén y llevarlo a otros laboratorios y facultades

---

## Correrlo en tu computadora

Para usarlo no necesitas nada de esto: basta con abrir **[khipu-fiee.streamlit.app](https://khipu-fiee.streamlit.app)**. Esto es para quien quiera revisar o mejorar el código.

```bash
git clone https://github.com/AldoRuiz07/KHIPU-.git
cd KHIPU-
python -m venv .venv
.venv\Scripts\activate            # en Mac o Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.ejemplo .env            # en Mac o Linux: cp .env.ejemplo .env
streamlit run app.py
```

En el archivo `.env` (o en los *Secrets* de Streamlit Cloud) van estas variables:

| Variable | Para qué sirve |
|---|---|
| `GEMINI_API_KEY` | Tu clave de [Google AI Studio](https://aistudio.google.com) (es gratuita) |
| `MODELOS` | Los modelos a usar, en orden y separados por comas |
| `CLAVE_ENCARGADO` | La clave del panel del encargado |
| `CORREO_REMITENTE` y `CORREO_CLAVE` | La cuenta de Gmail que envía los correos y su contraseña de aplicación |

---

## Lo que aprendimos

Khipu lo construimos en dos días para el hackathon ENEISOFT 2026. No ganamos, pero nos llevamos mucho más de lo que esperábamos:

- **Trabajar en equipo con Git.** Empezamos sin saber bien qué era clonar un repositorio. Aprendimos a repartir el código por módulos para no pisarnos, a hacer *pull* antes de *push* y por qué nunca hay que forzar un *push* sobre el trabajo de un compañero (lo aprendimos a la mala, y recuperamos el commit desde una copia local).
- **Cuidar las claves.** Una clave de API terminó por error en un archivo de ejemplo. La revocamos, separamos los secretos en `.env` y en los *Secrets* de Streamlit, y desde entonces nunca se suben al repositorio.
- **Que la IA no adivine.** La parte más valiosa no fue el modelo, sino obligarlo a consultar datos reales con herramientas y dejar las validaciones importantes (stock, horarios, cruces) a código normal.
- **Escuchar a los mentores.** La pregunta *"¿qué impide que alguien reserve a nombre de otro?"* nos llevó a la confirmación por correo y al sello digital, que terminaron siendo de lo mejor del proyecto.
- **Publicar temprano.** Subir la app a la nube desde el primer día nos permitió probarla en varias laptops y celulares a la vez, y encontrar errores que en local no aparecían.
- **Congelar el código a tiempo.** Cada cambio de último minuto reinicia la app y borra los datos de la demo. Fijar una hora de congelamiento y respetarla es parte del trabajo.

También usamos asistentes de IA para programar más rápido, revisar errores y preparar el pitch. Las decisiones de diseño, los datos del almacén y las equivalencias entre componentes las definimos y revisamos nosotros.

---

## Quiénes somos

Somos tres estudiantes de **Ingeniería Electrónica de San Marcos**. Más de una vez fuimos al almacén sin saber si había lo que buscábamos, compramos algo que la facultad ya tenía o llenamos solicitudes a mano. Khipu nació de eso.

<table align="center">
  <tr>
    <td align="center" width="240">
      <img src="assets/equipo/karla.png" width="120" alt="Karla Montes"><br>
      <b>Karla Montes</b><br>
      <sub>Base de datos y reservas de laboratorio</sub><br>
      <a href="https://www.linkedin.com/in/karlamontesm">LinkedIn</a>
    </td>
    <td align="center" width="240">
      <img src="assets/equipo/aldo.png" width="120" alt="Aldo Ruiz"><br>
      <b>Aldo Ruiz</b><br>
      <sub>Chat con IA, fotos y PDFs</sub><br>
      <a href="https://www.linkedin.com/in/aldoruiz07/">LinkedIn</a>
    </td>
    <td align="center" width="240">
      <img src="assets/equipo/erik.png" width="120" alt="Erik Espinel"><br>
      <b>Erik Espinel</b><br>
      <sub>Interfaz, Mi proyecto y panel del encargado</sub><br>
      <a href="https://www.linkedin.com/in/erik-espinel-bernilla">LinkedIn</a>
    </td>
  </tr>
</table>

<div align="center">

<br>

**Hecho pensando en la FIEE · Universidad Nacional Mayor de San Marcos**

</div>
