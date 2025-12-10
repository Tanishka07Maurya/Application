
// import React from 'react';
// import { Link } from 'react-router-dom';
// import Header from '../components/layout/Header';
// import Footer from '../components/layout/Footer';
// import Card from '../components/ui/Card';

// export default function HomePage() {
//   return (
//     <>
//       <Header />
//       <main className="flex flex-col items-center justify-center h-[80vh] bg-gray-50">
//         <Card className="text-center w-80">
//           <h2 className="text-xl font-bold mb-4">Welcome to Quiz Portal</h2>
//           <p className="mb-6 text-gray-600">Login or Sign Up to continue</p>
//           <div className="flex flex-col gap-3">
//             <Link to="/login" className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700">Login</Link>
//             <Link to="/signup" className="border border-blue-600 text-blue-600 py-2 rounded hover:bg-blue-50">Sign Up</Link>
//           </div>
//         </Card>
//       </main>
//       <Footer />
//     </>
//   );
// }

import React from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import './HomePage.css'; // import the CSS file

export default function HomePage() {
  return (
    <>
      <Header />
      <main className="homepage">
        <div className="card">
          <h2>Welcome to Quiz Portal</h2>
          <p>Login or Sign Up to continue</p>
          <div className="buttons">
            <Link to="/login" className="btn login-btn">Login</Link>
            <Link to="/Signup" className="btn signup-btn">Sign Up</Link>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
