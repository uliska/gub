--- guile-2.0.0.1/module/ice-9/boot-9.scm~	2011-03-13 23:21:07.000000000 +0100
+++ guile-2.0.0.1/module/ice-9/boot-9.scm	2011-03-17 20:30:32.817186829 +0100
@@ -3322,7 +3322,12 @@ module '(ice-9 q) '(make-q q-length))}."
         #f)))
 
   (define (absolute-path? path)
-    (string-prefix? "/" path))
+    (if (eq? (string-ref path 1) #\:)
+        ;; on Mingw, a file-name like X:/ is absolute
+        ;; obtain valid file name
+        (or (eq? (string-ref path 2) #\/)
+            (eq? (string-ref path 2) #\\))
+    (string-prefix? "/" path)))
 
   (define (load-absolute abs-path)
     (let ((cfn (let ((canon (false-if-exception (canonicalize-path abs-path))))
