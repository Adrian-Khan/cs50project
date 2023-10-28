# OpenEdVenture
#### Video Demo:  <https://youtu.be/HwyfxC3kJ-8>
#### Description:


Introduction:
Seeing that this web application, OpenEdVenture, was designed for CS50x, a free online course, I thought that I'd create a website that allows users to discover free online courses based on their interests. The platform lets users register, login, pick their interests from ~16 options (I plan to add more specific options in the future, as well as more courses to the database!) and then receive
a list of free courses that relate to those interests, which are then able to be filtered by level of difficulty and be favourited. These favourited courses and  interests are displayed on the user's homepage for easy access.

OpenEdVenture not only serves as a valuable resource for discovering free online courses but also demonstrates a commitment to providing a user-friendly, visually engaging, and responsive platform that enhances the learning journey.


Registration:
The first page as defined by the "/" route is the register page, as opposed to the homepage. I wanted this page to always be the one the user would first interact with as I added a description/introductory paragraph to the top so users can understand what the website is and what it does when first accessing OpenEdVenture. Then using JavaScript (JS) the user is scrolled automatically to the register form, or can click the arrow to do the same manually. To register the user provides a username, a password (min 8 characters with at least one symbol, letter and number) and password confirmation.


Login and Homepage:
Then after registering the user is redirected to login, and after doing so, lands on the actual homepage of the website, which greets the user, and displays a quote, their current interests as selected in the interest page, and their favourited courses as selected in the recommendations page. The navbar upon logging in displays 3 options: homepage, interests, and recommendations.


Interests page:
The interests page displays all of the interests the user can choose from. They were originally displayed as checkboxes but I used bootstrap and css to have them look like buttons (purely aesthetic choice). The page is split into 2 : the upper portion contains a list of all available interests, while the lower section showcases the user's current selections. TThis design enables users to conveniently select new interests from the upper list and deselect previously chosen ones from the lower section. These buttons are designed to change color and style upon being selected through utilising JS. When a checkbox is selected, the corresponding data is communicated to the Flask framework, updating the database tables tracking user interests. This functionality serves the dual purpose of managing the user's interests and populating relevant course recommendations on the homepage.


Recommendations page:
The recommendation page uses the user interests table to filter all the courses I have to only show those tagged with these interests. The user is also able to filter the courses with a select menu that, using JS, automatically submits the choice without the use of a button. The user is able to select a heart, that changes from just the outline to filled in when selected (done again using JS), which triggers an AJAX request to Flask that I use to populate the users favourite courses table, to then display these favourited courses on the homepage. The user is able to refresh the page and revisit it, always seeing favourites courses with the filled in heart, so they are able to, at anytime, edit their favourite courses by deselecting any of them to have these courses removed from their homepage.


Aesthetics and UI:
The colour scheme I choose was a gradient. I spent time experimenting wiht different color schemes, but ultimately picked a sunset themed palette to createa a welcoming and visually pleasing web application. Perhaps unusual for what is essentially at its core an informative website, but this design and UI was to ensure the aesthetics of the website were appealing and beautiful to prioritise the user experience. Similarly, I tried to think how I could make the website look better (less empty) and try figure how to code it, rather than thinking of what current css skills I had and using them to design the website. This helped me learn a lot of new ways to manipulate my websites, such as picking 'every other element' using :nth-of-type(2n). I also used media queries to ensure the design was responsive, and looks good on smaller screens as much as it looks good on a laptop. Note, the sign up card was stylised using this template tutorial : https://colorlib.com/wp/template/colorlib-regform-7/


Technologies:
Front-End: HTML, CSS, JavaScript, AJAX, Bootstrap
Back-End: Python/Flask
Database: SQLite
