import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

import ColorModeSwitcher from "./ColorModeSwitcher";
import HomeButton from "./HomeButton";

const Navbar = () => {
  const location = useLocation();
  const pathName = location.pathname;

  const navigate = useNavigate();

  return (
    <>
      {pathName !== "/" && pathName !== "/home" && (
        <HomeButton onClick={() => navigate("/")} />
      )}
      <ColorModeSwitcher justifySelf="flex-end" />
    </>
  );
};

export default Navbar;
