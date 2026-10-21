"use client";

import { useEffect, useRef } from "react";
import "swagger-ui-dist/swagger-ui.css";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/v1";
const SPEC_URL = `${API_URL.replace(/\/v1$/, "")}/openapi.json`;

// swagger-ui-dist já vem empacotado; o swagger-ui-react quebra no Turbopack
// (OpenApi3_1Element.refract is not a function) por causa do sideEffects do apidom.
export default function SwaggerViewer() {
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        let cancelled = false;
        import("swagger-ui-dist/swagger-ui-bundle.js").then(({ default: SwaggerUIBundle }) => {
            if (!cancelled && ref.current) SwaggerUIBundle({ url: SPEC_URL, domNode: ref.current });
        });
        return () => {
            cancelled = true;
        };
    }, []);

    return <div ref={ref} />;
}
