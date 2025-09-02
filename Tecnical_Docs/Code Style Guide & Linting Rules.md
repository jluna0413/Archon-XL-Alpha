## **Code Style Guide & Linting Rules**

* **Philosophy:** Code should be clean, readable, and consistent. We prioritize maintainability over premature optimization. All code must be auto-formatted on save.  
* **Backend (Python):**  
  * **Style Guide:** PEP 8\.  
  * **Formatter:** **Black** for uncompromising code formatting.  
  * **Linter:** **flake8** with plugins for security (bandit) and complexity (mccabe).  
  * **Example pyproject.toml snippet:**  
    Ini, TOML  
    \[tool.black\]  
    line-length \= 88  
    target-version \= \['py311'\]

    \[tool.flake8\]  
    max-line-length \= 88  
    extend-ignore \= "E203"

* **Frontend (TypeScript/React):**  
  * **Style Guide:** Airbnb JavaScript Style Guide.  
  * **Formatter:** **Prettier** for all formatting.  
  * **Linter:** **ESLint** with the Airbnb config, TypeScript plugins, and React hooks plugin.  
  * **Example .eslintrc.json snippet:**  
    JSON  
    {  
      "extends": \[  
        "airbnb",  
        "airbnb-typescript",  
        "plugin:prettier/recommended"  
      \],  
      "parserOptions": {  
        "project": "./tsconfig.json"  
      },  
      "rules": {  
        "react/react-in-jsx-scope": "off",  
        "react/jsx-props-no-spreading": "off"  
      }  
    }  
