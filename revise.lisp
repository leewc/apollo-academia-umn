;; constraint consists of variable list and function defining the constraint 
(defstruct constraint (vars NIL) (fn #'(lambda(x) x)))

;; revise() from book. removes only from (car vars). unary or binary input param.
(defun revise( inCons htable )
  ;; get domain values from first variable, whose domain might change
  (let ((d1 (gethash (car (constraint-vars inCons)) htable )))
    (print d1) ; useful for debugging
    ;; test arity of constraint - so far just unary and binary
    (if (eq 1 (list-length (constraint-vars inCons)))
	;; remove domain elements that do not meet unary constraint
	(setf (gethash (car (constraint-vars inCons)) htable )
	      (remove-if #'(lambda (x) (not (funcall (constraint-fn inCons) x )))
			 d1 ))
	)
      ;; remove domain elements from var1 that do not meet binary constraint
    (if (eq 2 (list-length (constraint-vars inCons)))
      (setf (gethash (car (constraint-vars inCons)) htable )
	    (remove-if #'(lambda(x)
			   ;; if all are null, x needs to be removed 
			   (every #'null 
				  (mapcar #'(lambda(y) (funcall (constraint-fn inCons) x y)) 
					  (gethash (cadr (constraint-vars inCons)) htable ))
				  ))  
		       d1 )
	   )
	)

    
    
   )
)
		

;; AC3 not fully functional - missing neighbors. 
;; For pie problem, need only run revise 2 times to complete  
(defun AC3 ( constraints vars )
  (dolist (c constraints)
    (revise c vars))
  (dolist (c constraints)
    (revise c vars))
  (maphash #'(lambda(k v)(print (list k v))) vars)
)

;;;; ------------------  BELOW is specific to PIE LOGIC ------------------
;; to run PIE LOGIC, (AC3 constraints people)

;; useful lists that define problem
(defparameter *pies* '(chocolate banana blueberry apple pecan))
(defparameter *people* '(rocky davis sam brandi mala))
(defparameter *fruit* '(banana blueberry apple))
(defparameter *dairy* '(chocolate banana))  

;; set domain of each person to all pies and collect in hash table
(setf people (make-hash-table))
(dolist (x *people*) (setf (gethash x people) *pies*)) 

; collect the constraints into a list
(defparameter allconstraints '())

;; make the "all different" binary constraints
(dolist (p *people*) 
  (dolist (q *people*) 
    (if ( not (eq p q)) 
	(setf allconstraints
	      (cons (make-constraint 
		       :vars (list p q)
		       :fn (lambda(x y) (not (eq x y)))
		       )
		      allconstraints )))))



;;; create the unary constraints ------
;; generic functions for fruit and dairy 
(defun notfruit (x) (not (member x *fruit*)))  
(defun notdairy (x) (not (member x *dairy*))) 
(defun yespecan (x) (eq x 'pecan) )
(defun notBlueBerry (x) (not (eq x 'blueberry)))
(defun notBanana (x) (not (eq x 'banana)))

;; sam ate pecan
;;(setf (gethash 'sam people) '(pecan))
(setf allconstraints 
      (cons (make-constraint
	     :vars (list 'sam) :fn #'yespecan)
	    allconstraints ))

;; rocky did not eat blueberry
;;(setf (gethash 'rocky people) (remove 'blueberry (gethash 'rocky people)))
(setf allconstraints 
      (cons (make-constraint
	     :vars (list 'rocky) :fn #'notBlueBerry)
	    allconstraints ))

;; davis did not eat banana
;;(setf (gethash 'davis people) (remove 'banana (gethash 'davis people)))
(setf allconstraints 
      (cons (make-constraint
	     :vars (list 'davis) :fn #'notBanana)
	    allconstraints ))

;; mala and rocky don't eat dairy
(setf allconstraints 
      (cons (make-constraint
	     :vars (list 'mala) :fn #'notdairy)
	    allconstraints ))
(setf allconstraints 
      (cons (make-constraint
	     :vars (list 'rocky) :fn #'notdairy)
	    allconstraints ))

;; sam and davis don't eat fruit
(setf allconstraints 
      (cons (make-constraint
	     :vars (list 'sam) :fn #'notfruit)
	    allconstraints ))
(setf allconstraints 
      (cons (make-constraint
	     :vars (list 'davis) :fn #'notfruit)
	    allconstraints ))

;; Running PIE logic
;;(AC3 allconstraints people)




;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;; ------------------  BELOW is specific to Robot LOGIC ------------------
;; to run Robot LOGIC, (AC3 robotConstraints robots)
 
;; useful lists that define problem
(defparameter *robots* '(red orange yellow green blue))
(defparameter *age* '(3 4 5 6 8))
 
;; set domain of each person to all pies and collect in hash table
(setf robots (make-hash-table))
(dolist (x *robots*) (setf (gethash x robots) *age*))
 
; collect the constraints into a list
(defparameter robotconstraints '())
 
;; make the "all different" binary constraints
(dolist (p *robots*)
  (dolist (q *robots*)
    (if ( not (eq p q))
        (setf robotconstraints
              (cons (make-constraint
                       :vars (list p q)
                       :fn (lambda(x y) (not (eq x y)))
                       )
                      robotconstraints )))))
 
 
;;; create the unary constraints ------
;; generic functions
(defun odd (x) (equal 1 (mod x 2)))  
(defun equalsfive (x) (equal x 5))
(defun olderoneoldertwo (x y z) (and (equal (+ 1 y) (x))
                                                                         (equal (+ 2 z) (x))))
 
;; Red's age is odd
;(setf robotconstraints
 ;     (cons (make-constraint
;            :vars (list 'red) :fn #'odd)
;           robotconstraints ))
;; Green 5
;(setf robotconstraints
 ;     (cons (make-constraint
;            :vars (list 'green) :fn #'equalsfive)
;           robotconstraints ))
 
;; Blue is 1 yr older than green
;; Blue is 2 yrs older then yellow
(setf robotconstraints
        (cons (make-constraint
                :vars(list 'blue 'green 'yellow) :fn #'olderoneoldertwo)
                robotconstraints))

(AC3 robotconstraints robots)
